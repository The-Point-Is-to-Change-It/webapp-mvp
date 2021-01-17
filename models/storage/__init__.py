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
    
    """
    SAVE OBJECT METHODS
    """
    
    def save_obj_to_db(self, obj):
        """ save an object to the db """
        Storage._db.collection(obj.__class__.__name__).document(obj.id).set(obj.__dict__)
    
    @classmethod
    def save_obj_to_db_with_dict(self, obj_dict):
        """ save an object to the db """
        Storage._db.collection(obj_dict.__class__.__name__).document(obj_dict.get('id')).set(obj_dict)
    
    """
    DELETE OBJECT METHODS
    """

    @classmethod
    def delete_from_db_with_dict(self, cls, dict_repr):
        """ delete an object from db """
        Storage._db.collection(cls.__name__).document(dict_repr['id']).delete()

    def delete_from_db(self, obj):
        """ delete an object from db """
        Storage._db.collection(obj.__class__.__name__).document(obj.id).delete()
    
    """
    GET OBJECT METHODS
    """

    def get_all(self, cls):
        """ get all objects of given class """
        return [ref.to_dict() for ref in Storage._db.collection(cls.__name__).get()]
    
    def get_n(self, cls, n):
        """ get n objects of given class """
        if n == 0:
            return {}
        ret = []
        for obj_ref in Storage._db.collection(cls.__name__).get():
            if len(ret) < n:
                ret.append(obj_ref.to_dict())
            else:
                break
        return ret
    '''
    def get_by_cls_and_attr(self, cls, attr, val):
        """ get first object in a given class that has a specified attr and value """
        # THIS NEEDS TO BE UPDATED TO NOT GET ALL DOCUMENTS IN A COLLECTION AND HAVE TO LOOP THROUGH
        ay = [ref.to_dict() for ref in Storage._db.collection(cls.__name__).get() if attr in ref.to_dict()]
        for each in ay:
            if each.get(attr) == val:
                return each
        return None
    '''

    def get_all_by_cls_and_attr(self, cls, attr, val):
        """ get all objects in given class that have specified attr and value """
        # THIS NEEDS TO BE UPDATED TO NOT GET ALL DOCUMENTS IN A COLLECTION AND HAVE TO LOOP THROUGH
        ay = [ref.to_dict() for ref in Storage._db.collection(cls.__name__).get() if attr in ref.to_dict()]
        ret = []
        for each in ay:
            if each.get(attr) == val:
                ret.append(each)
        return ret
    
    def get_n_by_cls_and_attr(self, cls, attr, val, n):
        """ get some number of objects in given class that have specified attr and value """
        # THIS NEEDS TO BE UPDATED TO NOT GET ALL DOCUMENTS IN A COLLECTION AND HAVE TO LOOP THROUGH
        val = val.lower()
        ay = [ref.to_dict() for ref in Storage._db.collection(cls.__name__).get() if attr in ref.to_dict()]
        ret = []
        for each in ay:
            if type(each.get(attr)) == str:
                if each.get(attr).lower() == val:
                    if len(ret) <= n:
                        ret.append(each)
                    else:
                        break
            elif each.get(attr) == val:
                if len(ret) <= n:
                    ret.append(each)
                else:
                    break
        return ret
    
    """
    UPDATE OBJECT METHODS
    """
    
    def update_attr_by_id(self, cls, id, attr, value):
        """ called only in base.py """
        Storage._db.collection(cls.__name__).document(id).update({attr: value})

    

storage = Storage()
