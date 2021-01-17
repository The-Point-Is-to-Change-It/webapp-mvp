"""
-----------------------------
  The Point Is to Change It | Routes - Landing
-----------------------------

Routes - Landing Contains:
1. all routes for the public landing page
2. calls api endpoints to interact with db

"""

from flask import Blueprint, render_template, request

landing = Blueprint("landing", __name__, url_prefix="")

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ public landing page """
    return render_template('/public/index.html', data={'error': request.args.get('error')})
