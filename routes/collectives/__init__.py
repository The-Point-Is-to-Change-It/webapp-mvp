"""
-----------------------------
  The Point Is to Change It | Routes - collectives
-----------------------------

Routes - collectives Contains:
1. all routes for interacting with/acting as a collectives 
2. calls api endpoints to interact with db

"""

from flask import Blueprint, render_template, redirect

collectives = Blueprint("collectives", __name__, url_prefix="/collectives")


@collectives.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ browse all collectives  """
    return redirect('dashboard.search')


@collectives.route('/', methods=['GET'], strict_slashes=False)
def profile(id):
    """ view a collective's public page """
    return render_template('/dash/public_profile.html')


@collectives.route('/<id>/2', methods=['GET'], strict_slashes=False)
def internal_dash(id):
    """ view a collective's internal dashboard  """
    return render_template('/private/collective.html')


@collectives.route('/auth/<col_id>/roles/<role_id>', methods=['GET'], strict_slashes=False)
def role(col_id, role_id):
    """ role within a collective's internal page """
    print('this is the role link')
    return render_template('/dash/role.html')
