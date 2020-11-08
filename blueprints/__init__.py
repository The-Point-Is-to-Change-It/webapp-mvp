"""
-----------------------------
  The Point Is to Change It - Blueprints
-----------------------------

Contained in /blueprints:
1. Flask blueprints representing routes and endpoints grouped by similarity 

"""
from blueprints.landing import home
from blueprints.auth import authenticate
from blueprints.auth.auth import Auth
from blueprints.auth.routes import *