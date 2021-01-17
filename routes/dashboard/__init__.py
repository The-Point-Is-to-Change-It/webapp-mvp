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
    from models.auth import Auth
    current_user = Auth.get_current_user()
    print(current_user)
    data = {
        'current_user': current_user,
        'full_view': request.full_view
    }
    return render_template('/dash/public_square.html', data=data)


@dash.route('/notifications', methods=['GET'], strict_slashes=False)
def notifications():
    """ main notifications page for users """
    from models.users import User
    user = User.get_n_by_cls_and_attr('id', request.current_user, 1)
    data = {
        'current_user': user,
        'full_view': request.full_view
    }
    return render_template('/dash/notifications.html', data=data)


@dash.route('/search', methods=['GET', 'POST'], strict_slashes=False)
def search():
    """ main notifications page for users """
    from models.users import User
    from models.collectives import Collective
    from models.auth import Auth
    # if entered search field
    data = {}
    user_input = request.form.get('user_input')
    found_users, found_collectives = [], []
    if user_input:
        # api requests to get users and collectives
        users_by_name_response = requests.get(build_url('api/users/name/' + str(user_input) + '/3'), data=request.form).json()
        users_by_handle_response = requests.get(build_url('api/users/handle/' + str(user_input) + '/3'), data=request.form).json()
        collectives_by_name_response = requests.get(build_url('api/collectives/name/' + str(user_input) + '/3'), data=request.form).json()
        collectives_by_handle_response = requests.get(build_url('api/collectives/handle/' + str(user_input) + '/3'), data=request.form).json()
        print(users_by_name_response)
        # add found collectives to list
        if collectives_by_handle_response.get('status') == 'OK':
            collectives_by_handle = collectives_by_handle_response.get('collectives')
            for collectives in collectives_by_handle:
                found_collectives.append(collectives)
        if collectives_by_name_response.get('status') == 'OK':
            collectives_by_name = collectives_by_name_response.get('collectives')
            for collectives in collectives_by_name:
                found_collectives.append(collectives)
        # add found users to list
        if users_by_handle_response.get('status') == 'OK':
            users_by_handle = users_by_handle_response.get('users')
            for users in users_by_handle:
                found_users.append(users)
        if users_by_name_response.get('status') == 'OK':
            users_by_name = users_by_name_response.get('users')
            for users in users_by_name:
                found_users.append(users)
    # if signed in - SHOULD BE IF AUTHENTICTED
    if request.current_user:
        current_user = Auth.get_current_user()
        if not found_users:
            users_response = requests.get(build_url('api/users/3'), data=request.form).json()
            users = users_response.get('users')
        else:
            users = found_users
        if not found_collectives:
            my_collectives = [Collective.get_n_by_cls_and_attr('id', each, 1) for each in current_user.get('collectives')]
        else:
            my_collectives = found_collectives
        data['current_user'] = current_user
        data['full_view'] = request.full_view
        data['collectives'] = my_collectives
        data['users'] = users
    else:
        if not found_users:
            users_response = requests.get(build_url('api/users/3'), data=request.form).json()
            users = users_response.get('users')
        else:
            users = found_users
        if not found_collectives:
            collectives_response = requests.get(build_url('api/collectives/3'), data=request.form).json()
            collectives = collectives_response.get('collectives')
        else:
            collectives = found_collectives
        data['users'] = users
        data['collectives'] = collectives
        data['full_view'] = request.full_view
        print('IN HERE')
    return render_template('/dash/search.html', data=data)


@dash.route('/create_collective', methods=['GET'], strict_slashes=False)
def create_collective():
    """ page with forms for creating a collective """
    from models.users import User
    user = User.get_n_by_cls_and_attr('id', request.current_user, 1)
    data = {
        'current_user': user,
        'full_view': request.full_view
    }
    return render_template('/dash/create_collective.html', data=data)
