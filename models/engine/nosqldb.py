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

class Data():
    """
    Get and set to and from the database
    """
    def __init__(self):
        """ initialize """
        pass

    @classmethod
    def get_user(self, email):
        """ get a user from the database using their email """
        users = db.collection(u'users')
        russ = users.document('russ')
        print(russ.get().to_dict())
        return ''