"""
-----------------------------
  The Point Is to Change It - Landing
-----------------------------

Contained in /landing:
1. Routes for the public landing page

"""

from blueprints.landing import home
from flask import render_template, jsonify

@home.route('/', methods=['GET'], strict_slashes=False)
def landing_page():
    """ Public Home Page """
    return render_template('public/landing.html')



