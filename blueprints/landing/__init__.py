"""
-----------------------------
  The Point Is to Change It - Landing
-----------------------------

Contained in /landing:
1. Routes and API endpoints for the public landing page

"""

from flask import Blueprint

home = Blueprint("home", __name__, url_prefix="")

from blueprints.landing.landing import *