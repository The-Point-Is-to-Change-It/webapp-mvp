"""
-----------------------------
  The Point Is to Change It - Bases Model
-----------------------------

Contained in Bases.py:
1. attributes and methods common to all other models,
    such as those associated with storage

"""

from flask import Flask, jsonify


class Base():
    """
    Base class
    """
    def __init__(self, *args, **kwargs):
        """ init """
        from models import db
        from uuid import uuid4
        self.id = str(uuid4())
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save()

    @classmethod
    def get_by_attr(cls, attr, value):
        """ get Base with an attribute that has given value """
        from models import db
        doc_ref = db.collection(cls.__name__).where(attr, '==', value)
        doc = doc_ref.get()
        if type(doc) == list:
            if len(doc) > 0:
                obj = cls(**doc[0].to_dict())
                return obj
        return None
    
    def save(self):
        """ save this Base object into the database """
        from models import db
        db.collection(self.__class__.__name__).document(self.id).set(self.__dict__)


