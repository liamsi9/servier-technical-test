import pandas as pd
from helpers.constants import END_BUCKET
from google.cloud import storage


def get_csv_header(csv_file):
    # reading the csv file using read_csv
    # storing the data frame in variable called df
    df = pd.read_csv(csv_file)

    return list(df.columns)


def upload_file():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(END_BUCKET)
    d = bucket.blob("test_pipeline")
    d.upload_from_string('V')