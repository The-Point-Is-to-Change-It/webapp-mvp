"""
-----------------------------
  The Point Is to Change It | Models - Storage
-----------------------------

Models - Storage Contains: 
1. Connection to the firestore database
2. Instantiation of the db client
3. Methods for interacting with the db

"""
from google.cloud import firestore



class Storage():
    """
    Get and set to and from the database
    """
    def __init__(self):
        """ initialize """
        # Project ID is determined by the GCLOUD_PROJECT environment variable
        self._db = firestore.Client()
    
    def save_obj_to_db(self, obj):
        """ save an object to the db """
        self._db.collection(obj.__class__.__name__).document(obj.id).set(obj.__dict__)
    
    def delete_from_db(self, obj):
        """ delete an object from db """
        self._db.collection(obj.__class__.__name__).document(obj.id).delete()
    
    def get_all(self, cls):
        """ get all objects of given class """
        return [ref.to_dict() for ref in self._db.collection(cls.__name__).get()]
    
    def get_by_cls_and_attr(self, cls, attr):
        """ get all objects in given class that have specified attribute """
        return [ref.to_dict() for ref in self._db.collection(cls.__name__).get() if attr in ref.to_dict()]

    
storage = Storage()
