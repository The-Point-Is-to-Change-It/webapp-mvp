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
    _db = firestore.Client()

    def __init__(self):
        """ initialize """
        # Project ID is determined by the GCLOUD_PROJECT environment variable
    
    def save_obj_to_db(self, obj):
        """ save an object to the db """
        Storage._db.collection(obj.__class__.__name__).document(obj.id).set(obj.__dict__)
    
    @classmethod
    def delete_from_db_with_dict(self, cls, dict_repr):
        """ delete an object from db """
        Storage._db.collection(cls.__name__).document(dict_repr['id']).delete()

    def delete_from_db(self, obj):
        """ delete an object from db """
        Storage._db.collection(obj.__class__.__name__).document(obj.id).delete()
    
    def get_all(self, cls):
        """ get all objects of given class """
        return [ref.to_dict() for ref in Storage._db.collection(cls.__name__).get()]
    
    def get_by_cls_and_attr(self, cls, attr, val):
        """ get all objects in given class that have specified attr and value """
        # THIS NEEDS TO BE UPDATED TO NOT GET ALL DOCUMENTS IN A COLLECTION AND HAVE TO LOOP THROUGH
        ay = [ref.to_dict() for ref in Storage._db.collection(cls.__name__).get() if attr in ref.to_dict()]
        for each in ay:
            if each.get(attr) == val:
                return each
        return None
    
    def update_attr_by_id(self, cls, id, attr, value):
        """ update object in db """
        Storage._db.collection(cls.__name__).document(id).update({attr: value})

    

storage = Storage()
