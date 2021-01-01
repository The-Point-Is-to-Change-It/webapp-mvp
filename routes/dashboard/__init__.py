"""
-----------------------------
  The Point Is to Change It | Routes - Dashboard
-----------------------------

Routes - Dashboard Contains:
1. all routes that for the internal dashboard
    * public square
    * notifications
    * search
2. calls api endpoints to interact with db

"""

from flask import Blueprint, render_template, g, request
import requests
from helpers import build_url


dash = Blueprint("dash", __name__, url_prefix="/dash")


@dash.route('/', methods=['GET'], strict_slashes=False)
def public_square():
    """ public square - neither private nor public page """
    from models.users import User
    user = User.get_by_cls_and_attr('id', request.current_user)
    data = {
        'current_user': user,
        'full_view': request.full_view
    }
    return render_template('/dash/public_square.html', data=data)


@dash.route('/notifications', methods=['GET'], strict_slashes=False)
def notifications():
    """ main notifications page for users """
    from models.users import User
    user = User.get_by_cls_and_attr('id', request.current_user)
    data = {
        'current_user': user,
        'full_view': request.full_view
    }
    return render_template('/dash/notifications.html', data=data)


@dash.route('/search', methods=['GET'], strict_slashes=False)
def search():
    """ main notifications page for users """
    from models.users import User
    user = User.get_by_cls_and_attr('id', request.current_user)
    data = {
        'current_user': user,
        'full_view': request.full_view
    }
    collectives = requests.get(build_url('api/collectives')).json()
    users = requests.get(build_url('api/users')).json()
    context = {
        'users': users,
        'collectives': collectives
    }
    return render_template('/dash/search.html', context=context, data=data)


@dash.route('/create_collective', methods=['GET'], strict_slashes=False)
def create_collective():
    """ page with forms for creating a collective """
    from models.users import User
    user = User.get_by_cls_and_attr('id', request.current_user)
    data = {
        'current_user': user,
        'full_view': request.full_view
    }
    return render_template('/dash/create_collective.html', data=data)
