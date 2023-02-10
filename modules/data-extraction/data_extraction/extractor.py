"""
Main function to extract data from bigquery.
"""

import traceback
from google.cloud import bigquery, firestore
from data_extraction.firestore_manager import FirestoreManager
from data_extraction.bigquery_manager import BigqueryManager

COLLECTION = "config"


class ExtractError(Exception):
    """
    Error in doing the sync.
    """

def extract(document_name):
    """
    Extract from bigquery
    """

    try:
        bigquery_client = bigquery.Client()
        bigquery_manager = BigqueryManager(bigquery_client)

        firestore_client = firestore.Client()
        firestore_manager = FirestoreManager(firestore_client)
        config = firestore_manager.get_config(COLLECTION, document_name)

        # step 4: sync ...
        bigquery_manager.extract(config.get('sql'))
    except Exception as err:
        raise ExtractError('internal error while extracting with the conf {} : {}\n{}'.format(
                document_name,
                str(err),
                traceback.format_exc()
            )
        )
