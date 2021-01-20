"""
-----------------------------
  The Point Is to Change It | Models - Base
-----------------------------

Models - Base Contains:
1. A base class definition to handle serialization and deserialization

"""

class Base():
    """ Base Model """
    def __init__(self, *args, **kwargs):
        """ init """
        from uuid import uuid4
        for (k, v) in kwargs.items():
            setattr(self, k, v)
        if not 'id' in kwargs.items():
            self.id = str(uuid4())

    def to_dict(self):
        """ return dictionary representation of object """
        return self.__dict__

    """
    GET METHODS
    """
    
    @classmethod
    def get_all(cls):
        """ get all objects of this class """
        from models.storage import storage
        print('in get all')
        return storage.get_all(cls)
    
    @classmethod
    def get_n(cls, n):
        """ get n objects of this class """
        from models.storage import storage
        return storage.get_n(cls, n)
    '''
    @classmethod
    def get_by_cls_and_attr(cls, attr, val):
        from models.storage import storage
        return storage.get_by_cls_and_attr(cls, attr, val)
    '''

    @classmethod
    def get_all_by_cls_and_attr(cls, attr, val):
        """ get all objects where attribute == value """
        from models.storage import storage
        return storage.get_all_by_cls_and_attr(cls, attr, val)
    
    @classmethod
    def get_n_by_cls_and_attr(cls, attr, val, n):
        """ get n objects where attribute == value """
        from models.storage import storage
        return storage.get_n_by_cls_and_attr(cls, attr, val, n)

    """
    POST METHODS
    """

    def save_to_db(self):
        from models.storage import storage
        storage.save_obj_to_db(self)

    @classmethod
    def save_to_db_with_dict(cls, obj_dict):
        from models.storage import storage
        storage.save_obj_to_db_with_dict(obj_dict)

    """
    DELETE METHODS
    """

    def delete_from_db(self):
        """ delete this object from db """
        from models.storage import storage
        storage.delete_from_db(self)

    @classmethod
    def delete_from_db_with_id(cls, id):
        """ delete this object from db """
        from models.storage import storage
        storage.delete_from_db_with_id(cls, id)

        
    
    """ REPLACE ALL OF THESE WITH METHODS THAT CORRESPOND TO API METHODS """

    
    @classmethod
    def get_all_or_n_cls(cls, n):
        response = None
        if not n:
            response = cls.get_all()
        else:
            response = cls.get_n(n)
        return response
    
    @classmethod
    def update_attr_by_id(cls, id, attr, value):
        """
        Update an object in the database by attribute and value
        
        USAGE: ------------------------------------------------

        From models.classname import Classname
        Classname.update_attr_by_id(object_id, attr_to_update, new_value)

        """
        from models.storage import storage
        return storage.update_attr_by_id(cls, id, attr, value)
    