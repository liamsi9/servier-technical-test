# Servier Technical Test

This module contains a dataflow that will ingest csv files in Bigquery and a data extraction module that will run a bigquery job and upload query results in a destination bucket as a json file.

## Description

The technical test follows this architecture:

- `Dataflow`      : A dataflow that will read drugs, pubmed, clinical trials files from a `servier-technical-test` bucket and save raw data in 3 bigquery tables: `drugs`, `pubmed` and `clinical_trials`. Tables are created via terraform from `database.tf` in iac folder. At the end of the dataflow, an empty file `test_pipeline` is created in `01-data-extraction` bucket. A pubsub notification  (see `notification.tf`) is created from this bucket and triggers a data extraction cloud function.

- `Data extraction CF` : This module will run a query and save a json file in a destination bucket (`01-data-extraction/output/output.json`). It is triggered once a file is uploaded to `01-data-extraction` bucket. The cloud function will read the file name, search for the corresponding document in firestore to get the query to execute. A bigquery job run the query and results are saved in output bucket. 


## Terraform infrastructure

This module creates several resources:
 - `database.tf`: create `drugs` , `pubmed` , `clinical_trials` and `output` tables
 - `iam.tf`: service account creation and roles attributions
 - `notification.tf`: creates pubsub topic and subscription
 - `storage.tf`: bucket creation
 - `workload.tf`: Cloud function that will run bigquery jobs


## Input parameters

In order to run the Servier technical test:
- Upload `drugs.csv`, `pubmed.csv`, `pubmed.json` and `clinical_trials.csv` to `gs://servier-technical-test`
- Create a firestore collection named `config` with a document `test_pipeline` that contains the following query:

```
SELECT
  DISTINCT drugs.drug AS drug,
  CAST(pubmed.id AS STRING) AS id,
  journal AS journal,
  pubmed.date AS date
FROM
  `servier-test-technique.servier_technical_test.drugs` AS drugs
INNER JOIN
  `servier-test-technique.servier_technical_test.pubmed` AS pubmed
ON
  LOWER(drugs.drug) IN UNNEST(REGEXP_EXTRACT_ALL(LOWER(REGEXP_REPLACE(pubmed.title, r',', ' ')),'[0-9a-zA-Z]+'))
UNION ALL (
  SELECT
    DISTINCT drugs.drug AS drug,
    clinical_trials.id AS id,
    journal AS journal,
    clinical_trials.date AS date
  FROM
    `servier-test-technique.servier_technical_test.drugs` AS drugs
  INNER JOIN
    `servier-test-technique.servier_technical_test.clinical_trials` AS clinical_trials
  ON
    LOWER(drugs.drug) IN UNNEST(REGEXP_EXTRACT_ALL(LOWER(REGEXP_REPLACE(clinical_trials.scientific_title, r',', ' ')),'[0-9a-zA-Z]+')) )
```

## Output
The output of this pipeline is a json file saved in `gs://01-data-extraction/output/output.json`.

````
[
    {"drug":"ETHANOL","id":"6","journal":"Psychopharmacology","date":"2020-01-01"},
    {"drug":"ATROPINE","journal":"The journal of maternal-fetal \u0026 neonatal medicine","date":"2020-03-01"},
    {"drug":"EPINEPHRINE","id":"8","journal":"The journal of allergy and clinical immunology. In practice","date":"2020-03-01"},
    {"drug":"EPINEPHRINE","id":"7","journal":"The journal of allergy and clinical immunology. In practice","date":"2020-02-01"},
    {"drug":"EPINEPHRINE","id":"NCT04188184","journal":"Journal of emergency nursing\\xc3\\x28","date":"2020-04-27"},
    {"drug":"ISOPRENALINE","id":"9","journal":"Journal of photochemistry and photobiology. B, Biology","date":"2020-01-01"},
    {"drug":"TETRACYCLINE","id":"5","journal":"American journal of veterinary research","date":"2020-01-02"},
    {"drug":"TETRACYCLINE","id":"4","journal":"Journal of food protection","date":"2020-01-01"},
    {"drug":"TETRACYCLINE","id":"6","journal":"Psychopharmacology","date":"2020-01-01"},
    {"drug":"BETAMETHASONE","id":"NCT04153396","journal":"Hôpitaux Universitaires de Genève","date":"2020-01-01"},
    {"drug":"BETAMETHASONE","id":"10","journal":"The journal of maternal-fetal \u0026 neonatal medicine","date":"2020-01-01"},
    {"drug":"BETAMETHASONE","journal":"The journal of maternal-fetal \u0026 neonatal medicine","date":"2020-03-01"},
    {"drug":"BETAMETHASONE","id":"11","journal":"Journal of back and musculoskeletal rehabilitation","date":"2020-01-01"},
    {"drug":"DIPHENHYDRAMINE","id":"NCT04189588","journal":"Journal of emergency nursing","date":"2020-01-01"},
    {"drug":"DIPHENHYDRAMINE","id":"1","journal":"Journal of emergency nursing","date":"2019-01-01"},
    {"drug":"DIPHENHYDRAMINE","id":"3","journal":"The Journal of pediatrics","date":"2019-01-02"},
    {"drug":"DIPHENHYDRAMINE","id":"NCT04237091","journal":"Journal of emergency nursing","date":"2020-01-01"},
    {"drug":"DIPHENHYDRAMINE","id":"2","journal":"Journal of emergency nursing","date":"2019-01-01"},
    {"drug":"DIPHENHYDRAMINE","id":"NCT01967433","journal":"Journal of emergency nursing","date":"2020-01-01"}
]

````


