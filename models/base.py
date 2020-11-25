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