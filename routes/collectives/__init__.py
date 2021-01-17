"""
-----------------------------
  The Point Is to Change It | Routes - collectives
-----------------------------

Routes - collectives Contains:
1. all routes for interacting with/acting as a collectives 
2. calls api endpoints to interact with db

"""

from flask import Blueprint, render_template, redirect, url_for, request
import requests
from helpers import build_url

collectives = Blueprint("collectives", __name__, url_prefix="/collectives")


@collectives.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ browse all collectives  """
    return redirect(url_for('dash.search'))


@collectives.route('/<id>', methods=['GET'], strict_slashes=False)
def profile(id):
    """ view a collective's public page """
    from models.auth import Auth
    current_user = Auth.get_current_user()
    collective = requests.get(build_url('api/collectives/' + id)).json()
    print(collective)
    data = {
        'current_user': current_user,
        'full_view': request.full_view,
        'collective': collective
    }
    return render_template('/dash/public_profile.html', data=data)


@collectives.route('/auth/<id>', methods=['GET'], strict_slashes=False)
def internal_dash(id):
    """ view a collective's internal dashboard  """
    from models.auth import Auth
    current_user = Auth.get_current_user()
    collective = requests.get(build_url('api/collectives/id/' + str(id))).json()
    data = {
        'current_user': current_user,
        'full_view': request.full_view,
        'collective': collective.get('collectives')
    }
    return render_template('/private/collective.html', data=data)


@collectives.route('/auth/<col_id>/roles/<role_id>', methods=['GET'], strict_slashes=False)
def role(col_id, role_id):
    """ role within a collective's internal page """
    return render_template('/dash/role.html')
