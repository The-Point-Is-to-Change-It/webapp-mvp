"""
-----------------------------
  The Point Is to Change It - Users Model
-----------------------------

Contained in users.py:
1. class definition for user entities

"""

from flask import Flask, jsonify
from models import Base


class User(Base):
    """
    User class
    """
    def __init__(self, *args, **kwargs):
        """ init """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        self.handle = kwargs.get('handle')
        self.password = kwargs.get('password')
    
    def check_password(self, password):
        """ validate password for login """
        return True if password == self.password else False