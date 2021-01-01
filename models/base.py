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
    
    def save_to_db(self):
        from models.storage import storage
        storage.save_obj_to_db(self)
    
    def delete_from_db(self):
        """ delete this object from db """
        from models.storage import storage
        storage.delete_from_db(self)
    
    @classmethod
    def delete_from_db_with_dict(cls, dict_repr):
        """ delete this object from db """
        from models.storage import storage
        storage.delete_from_db_with_dict(cls, dict_repr)
    
    @classmethod
    def get_all(cls):
        """ retrieve objects of same class """
        from models.storage import storage
        return storage.get_all(cls)
    
    @classmethod
    def get_by_cls_and_attr(cls, attr, val):
        from models.storage import storage
        return storage.get_by_cls_and_attr(cls, attr, val)
    
    @classmethod
    def update_attr_by_id(cls, id, attr, value):
        from models.storage import storage
        return storage.update_attr_by_id(cls, id, attr, value)
    