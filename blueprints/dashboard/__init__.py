"""
-----------------------------
  The Point Is to Change It - Dashboard
-----------------------------

Contained in /dashboard:
1. 

"""
from flask import Blueprint

dash = Blueprint("dashboard", __name__, url_prefix="/dashboard")

from blueprints.dashboard.routes import *
