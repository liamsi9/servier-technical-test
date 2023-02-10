"""
Main module for GCF data extraction
"""

import base64
import json
import logging
import traceback

from google.cloud import error_reporting

from data_extraction.extractor import extract


logger = logging.getLogger('data-extraction')



def main(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    print('*' * 100)
    print(pubsub_message)
    extract(pubsub_message["name"])

