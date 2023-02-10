"""Firestore manager."""



class FirestoreManager:
    """Firestore manager."""

    def __init__(self, firestore_client):
        """Init the firestore manager."""
        self.firestore_client = firestore_client

    def get_config(self, collection, doc):
        """
        List documents from a collection.

        Args:
            collection: name of the collection in firestore
        """
        doc_ref = self.firestore_client.collection(collection).document(doc)
        config = doc_ref.get().to_dict()

        return  config

