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
    def save_obj_to_db_with_dict(cls, cls_name, obj_dict):
        """ save an object to the db """
        Storage._db.collection(cls_name).document(obj_dict.get('id')).set(obj_dict)
    
    


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

    
    def get_n_by_cls_and_attr(self, cls, attr, val, n=None):
        """ get some number of objects in given class that have specified attr and value """
        # THIS NEEDS TO BE UPDATED TO NOT GET ALL DOCUMENTS IN A COLLECTION AND HAVE TO LOOP THROUGH
        val = val.lower()
        all_found = [ref.to_dict() for ref in Storage._db.collection(cls.__name__).get() if attr in ref.to_dict()]
        ret = []
        if not n:
            n = len(all_found)
        for each in all_found:
            if type(each.get(attr)) == str:
                if each.get(attr).lower() == val or val in each.get(attr):
                    if len(ret) < n:
                        ret.append(each)
                    else:
                        break
            elif each.get(attr) == val or val in each.get(attr):
                if len(ret) < n:
                    ret.append(each)
                else:
                    break
        return ret
    
    """
    UPDATE OBJECT METHODS
    """
    
    def update_attr_by_id(self, cls, id, attr, value):
        """ called only in base.py """
        ALLOWED_CLASSES = ['User', 'Collective', 'Role', 'Will', 'Authority']
        ref = Storage._db.collection(cls.__name__).document(id)
        obj = cls.get_n_by_cls_and_attr('id', id, 1) if cls.__name__ in ALLOWED_CLASSES else None
        if obj:
            if type(obj[0].get(attr)) == list:
                ref.update({attr: firestore.ArrayUnion([value])})
                return
        ref.update({attr: value})

    """
    DELETE OBJECT METHODS
    """

    @classmethod
    def delete_from_db_with_id(self, cls, id):
        """ usage: storage.delete_from_db_with_id('User', user_id) """
        print('in storage delete')
        Storage._db.collection(cls.__name__).document(id).delete()

    def remove_attr_value(self, cls, id, attr, value):
        """ called only in base.py """
        ALLOWED_CLASSES = ['User', 'Collective', 'Role', 'Will', 'Authority']
        ref = Storage._db.collection(cls.__name__).document(id)
        obj = cls.get_n_by_cls_and_attr('id', id, 1) if cls.__name__ in ALLOWED_CLASSES else None
        if obj:
            if type(obj[0].get(attr)) == list:
                print('type is list')
                ref.update({attr: firestore.ArrayRemove([value])})
                return
        print('should not be here')
        ref.update({attr: value})
        

    

storage = Storage()
