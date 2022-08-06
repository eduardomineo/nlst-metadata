# NLST Metadata
# 
# eduardomineo@gmail.com
# INCOR/FMUSP, Brazil
# 2022
#
# build.py: Build the Relational Database
#
import os
import json
import traceback

from glob import glob
from tqdm import tqdm

import sqlite3 as sl

DB_PATH='db/nlst.db'

#
#
def create_tables(conn):
    conn.execute('''
        CREATE TABLE SERIES (
            series_id INTEGER NOT NULL PRIMARY KEY,
            series_uid TEXT,
            series_number TEXT,
            series_description TEXT,
            series_number_images INTEGER,
            series_modality TEXT,
            series_manufacturer TEXT,
            series_model TEXT,
            series_annotations_flag BOOLEAN,
            series_annotations_size INTEGER,
            series_total_size INTEGER,
            series_project TEXT,
            series_data_provenance TEXT,
            series_software_version TEXT,
            series_max_frame_count INTEGER,
            series_body_part TEXT,
            series_third_party_analysis TEXT,
            series_description_uri TEXT,
            series_sop_class_uid TEXT,
            series_license_name TEXT,
            series_license_url TEXT,
            series_commercial_restrictions BOOLEAN,
            series_exact_size INTEGER,
            series_screening_year INTEGER,
            series_image_type TEXT,
            series_convolution_kernel TEXT,
            series_reconstruction_diameter REAL,
            series_slice_thickness REAL,
            series_kvp REAL,
            series_mas REAL,
            series_effective_mas REAL,
            series_pitch REAL,

            patient_id INTEGER,
            patient_subject_id INTEGER,

            study_id INTEGER,
            study_uid TEXT,
            study_date INTEGER,
            study_description TEXT,
            study_exclude_commercial TEXT
        );
    ''')
    conn.execute('''
        CREATE INDEX idx_pat_id ON SERIES(patient_id);
    ''')
    conn.execute('''
        CREATE INDEX idx_std_id ON SERIES(study_id);
    ''')

#
#
def insert_series(conn, patient, study, seriesList):
    query = '''
            INSERT INTO SERIES(
                series_id,
                series_uid,
                series_number,
                series_description,
                series_number_images,
                series_modality,
                series_manufacturer,
                series_model,
                series_annotations_flag,
                series_annotations_size,
                series_total_size,
                series_project,
                series_data_provenance,
                series_software_version,
                series_max_frame_count,
                series_body_part,
                series_third_party_analysis,
                series_description_uri,
                series_sop_class_uid,
                series_license_name,
                series_license_url,
                series_commercial_restrictions,
                series_exact_size,
                series_screening_year,
                series_image_type,
                series_convolution_kernel,
                series_reconstruction_diameter,
                series_slice_thickness,
                series_kvp,
                series_mas,
                series_effective_mas,
                series_pitch,
                patient_id,
                patient_subject_id,
                study_id,
                study_uid,
                study_date,
                study_description,
                study_exclude_commercial
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    '''

    data = []

    for series in seriesList:
        additional_values = series['description'].split(',')
        while len(additional_values) < 11:
            additional_values.append('null')

        modelName = series['manufacturerModelName'];
        if modelName is None:
            modelName = additional_values[3]

        data.append((
            series['seriesPkId'],
            series['seriesUID'],
            series['seriesNumber'],
            series['description'],
            series['numberImages'],
            series['modality'],
            series['manufacturer'],
            modelName,
            series['annotationsFlag'],
            series['annotationsSize'],
            series['totalSizeForAllImagesInSeries'],
            series['project'],
            series['dataProvenanceSiteName'],
            series['softwareVersion'],
            series['maxFrameCount'],
            series['bodyPartExamined'],
            series['thirdPartyAnalysis'],
            series['descriptionURI'],
            series['sopClassUID'],
            series['licenseName'],
            series['licenseUrl'],
            series['commercialRestrictions'],
            series['exactSize'],
            additional_values[0],
            additional_values[1],
            additional_values[4],
            strToFloat(additional_values[5]),
            strToFloat(additional_values[6]),
            strToFloat(additional_values[7]),
            strToFloat(additional_values[8]),
            strToFloat(additional_values[9]),
            strToFloat(additional_values[10]),

            patient['id'],
            patient['subjectId'],

            study['id'],
            study['studyId'],
            study['date'],
            study['description'],
            study['excludeCommercial']
        ))

    conn.executemany(query, data)

def strToFloat(s):
    try:
        return float(s)
    except:
        return None

#
#
def import_files(conn):
    patient_files = glob('./patient/*.json')

    for patient_file in tqdm(patient_files):
        basename = os.path.basename(patient_file)
        result_id = os.path.splitext(basename)[0]

        f = open(patient_file, 'r')
        result_set  = json.load(f)['resultSet']

        for patient in result_set:
            subject_id = patient['subjectId']
            for study_ident in patient['studyIdentifiers']:
                study_identifier = study_ident['studyIdentifier']

                study_file = os.path.join('studies', result_id, subject_id, f'{study_identifier}.json')

                s = open(study_file, 'r')
                study = json.load(s)

                if len(study) > 1:
                    raise Exception(f'{study_file} contains {len(study)}')

                study = study[0]

                insert_series(conn, patient, study, study['seriesList'])

#
#
def main():
    print('NLST metadata database builder')
    print()

    try:
        db_dirname = os.path.dirname(DB_PATH)
        if not os.path.exists(db_dirname):
            os.makedirs(db_dirname)

        if os.path.exists(DB_PATH):
            raise Exception(f'Database file {DB_PATH} already exists')

        with sl.connect(DB_PATH) as conn:
            create_tables(conn)
            import_files(conn)

        print(f'Database created on {DB_PATH}')
    except Exception:
        print(traceback.format_exc())

#
# Program entry-point
if __name__ == '__main__':
    main()
