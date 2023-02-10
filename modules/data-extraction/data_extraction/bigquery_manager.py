"""Bigquery Helper to load and query."""

import json
import logging

from google.cloud import bigquery

PROJECT = "servier-test-technique"
DATASET = 'servier_technical_test'
TABLE = 'output'
EXTRACTION_BUCKET = "01-data-extraction"

class BigqueryManagerError(Exception):
    """Error occurs while creating BigQuery jobs."""


class BigqueryManager:
    """Bigquery encapsulation to load file."""

    def __init__(self, bigquery_client):  # pragma: no cover
        """Create a BigQueryHelper."""
        self.bigquery_client = bigquery_client

    def extract(self, sql):  # pragma: no cover
        """Run a Query in BigQuery.

        Args:
            sql: Query to execute

        Returns:
            BigQuery job id
        """
        client = bigquery.Client()

        # Write query results to a new table
        job_config = bigquery.QueryJobConfig()
        table_ref = client.dataset(DATASET).table(TABLE)
        job_config.destination = table_ref
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

        query_job = client.query(
            sql,
            location='EU',  # Location must match dataset
            job_config=job_config)
        rows = list(query_job)  # Waits for the query to finish

        # Export table to GCS
        destination_uri = "gs://{}/{}".format(EXTRACTION_BUCKET, "output/output.json")
        dataset_ref = bigquery.DatasetReference(PROJECT, DATASET)
        table_ref = dataset_ref.table(TABLE)
        job_config = bigquery.job.ExtractJobConfig()
        job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON

        extract_job = client.extract_table(
            table_ref,
            destination_uri,
            job_config=job_config,
            # Location must match that of the source table.
            location="EU",
        )  # API request
        extract_job.result()  # Waits for job to complete.
