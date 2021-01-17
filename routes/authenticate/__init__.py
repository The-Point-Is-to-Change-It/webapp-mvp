"""
-----------------------------
  The Point Is to Change It | Routes - authenticate
-----------------------------

Routes - authenticate Contains:
1. all routes for registering, logging in, and logging out
2. calls api endpoints to interact with Auth class and db

"""

from flask import Blueprint, render_template, redirect, url_for, request, jsonify, make_response
import requests
from helpers import build_url

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """ browse all authenticate  """
    from models.users import User
    new_user = requests.post(build_url('api/users'), data=request.form).json()
    if new_user.get('status') == 'error':
        print('failed to make user')
        return redirect(url_for('landing.index', error=new_user.get('message')))
    response = requests.post(build_url('api/sessions'), data=request.form).json()
    if not response:
        return redirect(url_for('landing.index', data={'error': 'API failure. Please try again later.'}))
    if response.get('status') == 'error':
        return redirect(url_for('landing.index', data={'error': response.get('message')}))
    user = User.get_n_by_cls_and_attr('id', response.get('user').get('id'), 1)
    data = {
        'user': user,
        'current_user': user,
        'full_view': request.full_view,
        'message': "Welcome! Let's get started."
    }
    res = make_response(render_template('/dash/account.html', data=data))
    res.set_cookie('session', response.get('id'))
    return res


@auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """ browse all authenticate  """
    from models.users import User
    from models.auth.session import Session
    response = requests.post(build_url('api/sessions'), data=request.form).json()
    if not response:
        return redirect(url_for('landing.index', data={'error': 'API failure. Please try again later.'}))
    if response.get('status') == 'error':
        return redirect(url_for('landing.index', data={'error': response.get('message')}))
    user = response.get('user')
    data = {
        'user': user,
        'current_user': user,
        'full_view': request.full_view
    }
    res = make_response(render_template('/dash/account.html', data=data))
    res.set_cookie('session', response.get('id'))
    return res


@auth.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """ delete current user session """

    requests.delete(build_url('api/sessions'), data=request.cookies).json()

    data = {
        'user': None,
        'current_user': None,
        'full_view': request.full_view
    }

    response = make_response(render_template('/public/index.html', data=data))
    return response


