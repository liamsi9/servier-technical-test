import apache_beam as beam
from helpers.constants import BUCKET


class ReadFileContent(beam.DoFn):
    """Custom reader to read a file from gcs"""
    def setup(self):
        from google.cloud import storage
        self.storage_client = storage.Client()

    def process(self, file_name):
        bucket = self.storage_client.get_bucket(BUCKET)
        blob = bucket.get_blob(file_name)
        yield blob.download_as_string()
