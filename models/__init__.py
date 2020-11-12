"""
-----------------------------
  The Point Is to Change It - Models
-----------------------------

Contained in /models:
1. Python Models
2. Storage Engine (NoSQL - Firestore)

"""

from models.engine.nosqldb import db, Data
from models.base import Base
from models.user import User
from models.session import Session
