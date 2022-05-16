# National Lung Screening Trial
NLST is a dataset of low-dose chest CT DICOM images and its metadata. Further information about the dataset can be found at [National Lung Screening Trial Public Access](https://wiki.cancerimagingarchive.net/display/NLST/National+Lung+Screening+Trial).

# This project
NLST dataset is a powerful tool for medical image researchers since it comprehends a wide range of patients, institutions, acquisition parameters and equipments. In order to download DICOM images with [NBIA Data Retriever](https://wiki.cancerimagingarchive.net/display/NBIA/Downloading+TCIA+Images), a manifest file containing series identifiers must be created. This can be achieved using the [NBIA search website](https://nlst.cancerimagingarchive.net/nbia-search/) whether through its simple search or its text search. However, researchers may find challenging defining their cohorts with more complex criteria such as numerical comparisons (for instance, studies with slice thickness greater than 2mm) or grouping conditions (for instance, studies with more than 2 series) or more ad-hoc selection (for instance, only one study per patient ordered by number of images).

This project provides a Python 3 script to create a local relational database (SQLite DB) from downloaded NLST DICOM Metadata. Once the database is created, researchers can use any SQLite client ([DBeaver](https://dbeaver.io/download/), for instance) to execute SQL queries.

Metadata was downloaded according to the following criteria:

* Collection: NLST
* Image modality: CT
* Anatomical site: CHEST
* Exclude Phantoms
* Exclude 3rd-Party Results
* Exclude collections with commercial use restrictions


* Total subjects: 25,970
* Total studies: 70,817
* Total series: 194,309
* Total images (count only): 20,266,972


# Data structure

Table: **SERIES**
|Column                         | Data Type | Modifiers            |
|:------------------------------|:----------|:---------------------|
|series_id                      | INTEGER   | NOT NULL PRIMARY KEY |
|series_uid                     | TEXT      |                      |
|series_number                  | TEXT      |                      |
|series_description             | TEXT      |                      |
|series_number_images           | INTEGER   |                      |
|series_modality                | TEXT      |                      |
|series_manufacturer            | TEXT      |                      |
|series_model                   | TEXT      |                      |
|series_annotations_flag        | BOOLEAN   |                      |
|series_annotations_size        | INTEGER   |                      |
|series_total_size              | INTEGER   |                      |
|series_project                 | TEXT      |                      |
|series_data_provenance         | TEXT      |                      |
|series_software_version        | TEXT      |                      |
|series_max_frame_count         | INTEGER   |                      |
|series_body_part               | TEXT      |                      |
|series_third_party_analysis    | TEXT      |                      |
|series_description_uri         | TEXT      |                      |
|series_sop_class_uid           | TEXT      |                      |
|series_license_name            | TEXT      |                      |
|series_license_url             | TEXT      |                      |
|series_commercial_restrictions | BOOLEAN   |                      |
|series_exact_size              | INTEGER   |                      |
|series_screening_year          | INTEGER   |                      |
|series_image_type              | TEXT      |                      |
|series_convolution_kernel      | TEXT      |                      |
|series_reconstruction_diameter | REAL      |                      |
|series_slice_thickness         | REAL      |                      |
|series_kvp                     | REAL      |                      |
|series_mas                     | REAL      |                      |
|series_effective_mas           | REAL      |                      |
|series_pitch                   | REAL      |                      |
|patient_id                     | INTEGER   |                      |
|patient_subject_id             | INTEGER   |                      |
|study_id                       | INTEGER   |                      |
|study_uid                      | TEXT      |                      |
|study_date                     | INTEGER   |                      |
|study_description              | TEXT      |                      |



# Usage

```
$ git clone git@github.com:eduardomineo/nlst-metadata.git
$ python build.py
NLST metadata database builder

Database created on db/nlst.db
```

Once the database is created, you can connect to it and execute SQL queries.

```
SELECT COUNT(DISTINCT PATIENT_ID) FROM SERIES;
***
COUNT(DISTINCT PATIENT_ID)|
--------------------------+
                     25970|
```

```
SELECT COUNT(DISTINCT STUDY_ID) FROM SERIES;
***
COUNT(DISTINCT STUDY_ID)|
------------------------+
                   70817|
```

```
SELECT COUNT() FROM SERIES;
***
COUNT()|
-------+
 194309|
```

```
SELECT SUM(series_number_images) FROM SERIES;
***
SUM(series_number_images)|
-------------------------+
                 20266972|
```

```
SELECT COUNT(*) FROM SERIES WHERE series_slice_thickness >= 2 and series_slice_thickness  <= 3
***
COUNT(*)|
--------+
  100948|
```


# Manifest file example
In order to download DICOM files, you need to create a Manifest file and import it using [NBIA Data Retriever](https://wiki.cancerimagingarchive.net/display/NBIA/Downloading+TCIA+Images). The Manifest structure is demonstrated below. Replace the list of ListOfSeriesToDownload with a list of `series_uid` from your SQL result.

```
downloadServerUrl=https://nlst.cancerimagingarchive.net/nbia-download/servlet/DownloadServlet
includeAnnotation=true
noOfrRetry=4
databasketId=manifest.tcia
manifestVersion=3.0
ListOfSeriesToDownload=
1.2.840.113654.2.55.229650531101716203536241646069123704792
1.2.840.113654.2.55.257926562693607663865369179341285235858
1.2.840.113654.2.55.21461438679308812574178613217680405233
1.2.840.113654.2.55.283399418711252976131557177419186072875
1.2.840.113654.2.55.107058971791399096468046631579934786083
1.2.840.113654.2.55.122344168497038128022524906545138736420
1.2.840.113654.2.55.97114726565566537928831413367474015470
```


# Citations & Data Usage Policy

Users of this data must abide by the [TCIA Data Usage Policy](https://wiki.cancerimagingarchive.net/x/c4hF) and the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/) under which it has been published. Attribution should include references to the following citations:

> **Dataset Citation**
>
> National Lung Screening Trial Research Team. (2013). **Data from the National Lung Screening Trial (NLST) [Data set]**. The Cancer Imaging Archive. [https://doi.org/10.7937/TCIA.HMQ8-J677](https://doi.org/10.7937/TCIA.HMQ8-J677)

> **Publication Citation**
>
> National Lung Screening Trial Research Team*; Aberle DR, Adams AM, Berg CD, Black WC, Clapp JD, Fagerstrom RM, Gareen IF, Gatsonis C, Marcus PM, Sicks JD (2011). **Reduced Lung-Cancer Mortality with Low-Dose Computed Tomographic Screening**. New England Journal of Medicine, 365(5), 395–409. [https://doi.org/10.1056/nejmoa1102873](https://doi.org/10.1056/nejmoa1102873)
>
> *note:  [List of National Lung Screening Trial members (pages 1-31 of this supplemental PDF to this article](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4356534/bin/NIHMS320819-supplement-Supplement1.pdf)

> **TCIA Citation**
>
> Clark K, Vendt B, Smith K, Freymann J, Kirby J, Koppel P, Moore S, Phillips S, Maffitt D, Pringle M, Tarbox L, Prior F. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository, Journal of Digital Imaging, Volume 26, Number 6, December, 2013, pp 1045-1057. DOI: [https://doi.org/10.1007/s10278-013-9622-7](https://doi.org/10.1007/s10278-013-9622-7)
