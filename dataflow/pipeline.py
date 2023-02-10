"""Dataflow pipeline to read files and save into bigquery"""

import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, WriteToBigQuery

from helpers.constants import (
    PROJECT_NAME,
    DESTINATION_DATASET,
    DRUGS_TABLE,
    PUBMED_TABLE,
    CLINICAL_TRIALS_TABLE,
    BUCKET
)
from helpers.utils import get_csv_header, upload_file
from transforms.date import ConvertDateFormat
from transforms.data_ingestion import DataIngestion
from transforms.readers import ReadFileContent



def run(argv=None):
    # Define pipeline options
    pipeline_options = PipelineOptions(
        runner="DataflowRunner",
        project="servier-test-technique",
        region="europe-west1",
        job_name="servier",
        temp_location=f"gs://{BUCKET}/tmp",
        staging_location=f"gs://{BUCKET}/staging",
        setup_file= "./setup.py"
    )

    data_ingestion = DataIngestion()

    # Create the pipeline
    with beam.Pipeline(options=pipeline_options) as pipeline:
        drug_headers = get_csv_header(f'gs://{BUCKET}/drugs.csv')
        pubmed_headers = get_csv_header(f'gs://{BUCKET}/pubmed.csv')
        clinical_trials_headers = get_csv_header(f'gs://{BUCKET}/clinical_trials.csv')

        drugs = (
            pipeline
                | 'Read Drugs CSV' >> ReadFromText(f'gs://{BUCKET}/drugs.csv', skip_header_lines=1)
                | 'String To BigQuery Row' >> beam.Map(lambda s: data_ingestion.parse_method(s, drug_headers))
                | 'Write drugs to BigQuery' >> beam.io.WriteToBigQuery(
                    table=f'{PROJECT_NAME}:{DESTINATION_DATASET}.{DRUGS_TABLE}',
                    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
                )
        )

        pubmed_csv = (
            pipeline
                | 'Read Pubmed CSV' >> ReadFromText(f'gs://{BUCKET}/pubmed.csv', skip_header_lines=1)
                | 'Parse Pubmed CSV' >> beam.Map(
                lambda s: data_ingestion.parse_method(s, pubmed_headers)
                )
                | beam.Filter(lambda x: x is not None)
                | 'Convert pubmed csv date format' >> beam.ParDo(ConvertDateFormat())
        )

        pubmed_json = (
            pipeline
                | 'Read Pubmed JSON' >> beam.Create(["pubmed.json"])
                | 'Read each file content' >> beam.ParDo(ReadFileContent())
                | 'Decode2' >> beam.Map(lambda x: json.loads(x))
                | 'Convert pubmed json date format' >> beam.ParDo(ConvertDateFormat())
        )

        pubmed = (pubmed_csv, pubmed_json) | 'Flatten pubmed' >> beam.Flatten()
        pubmed | 'Write pubmed JSON to BigQuery' >> WriteToBigQuery(
                    f'{PROJECT_NAME}:{DESTINATION_DATASET}.{PUBMED_TABLE}',
                    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
                )

        clinical_trials = (
            pipeline
                | 'Read clinical trials CSV' >> ReadFromText(f'gs://{BUCKET}/clinical_trials.csv', skip_header_lines=1)
                | 'Parse clinical trials CSV' >> beam.Map(
                    lambda s: data_ingestion.parse_method(s, clinical_trials_headers)
                )
                | beam.Filter(lambda x: x is not None)
                | 'Convert clinical trials csv date format' >> beam.ParDo(ConvertDateFormat())
                | 'Write clinical_trials to BigQuery' >> beam.io.WriteToBigQuery(
                    table=f'{PROJECT_NAME}:{DESTINATION_DATASET}.{CLINICAL_TRIALS_TABLE}',
                    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
                )
        )

        result = pipeline.run()
        result.wait_until_finish()
        upload_file()




if __name__ == '__main__':
    run()
