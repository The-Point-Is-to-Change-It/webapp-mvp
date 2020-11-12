"""
-----------------------------
  The Point Is to Change It - Auth
-----------------------------

Contained in /auth:
1. 

"""


from flask import Blueprint

authenticate = Blueprint("auth", __name__, url_prefix="/auth")

from blueprints.auth.routes import *
from blueprints.auth.api import *
from blueprints.auth.auth import *
