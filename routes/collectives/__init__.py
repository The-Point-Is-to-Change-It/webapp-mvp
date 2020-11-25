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


@collectives.route('/<id>/', methods=['GET'], strict_slashes=False)
def profile(id):
    """ view a collective's public page or internal dashboard depending on permissions """
    return render_template('/dash/collective.html')


@collectives.route('/<id>/role', methods=['GET'], strict_slashes=False)
def role(id):
    """ collectives page """
    print('this is the role link')
    return render_template('/dash/role.html', id=id)
