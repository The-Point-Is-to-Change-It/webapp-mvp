"""
-----------------------------
  The Point Is to Change It
-----------------------------

Contains: 
1. Connection to the firestore database
2. Instantiation of the db client

"""
from google.cloud import firestore


# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

