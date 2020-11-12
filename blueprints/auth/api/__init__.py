"""
-----------------------------
  The Point Is to Change It - Auth API
-----------------------------

Contained in /auth/api:
1. 


TO DO:
1. return appropriate error response codes
"""

from blueprints.auth import authenticate
from flask import request, render_template, jsonify


@authenticate.route('/api/register', methods=['POST', 'GET'], strict_slashes=False)
def api_register():
    """ check if email and handle are unique
            Failure: return error message
            Success: register a new user
    """
    from models import User

    # get registration information from form
    email, handle = request.form.get('email'), request.form.get('handle')
    username, pwd = request.form.get('username'), request.form.get('password')

    # ensure all registration information is present
    if not email or not handle or not username or not pwd:
        return jsonify({
            'status': 'error',
            'message': 'please fill out registration form'
        })

    # ensure email and handle are unique, if not present error
    if User.get_by_attr('email', email):
        return jsonify({
            'status': 'error',
            'message': 'email already in use'
        })
    if User.get_by_attr('handle', handle):
        return jsonify({
            'status': 'error',
            'message': 'handle already in use'
        })
    
    # create a new user
    kwargs = {
        'email': email,
        'handle': handle,
        'username': username,
        'password': pwd
        }
    new_user = User(**kwargs)
    return jsonify({
        'status': 'success',
        'message': ''
    })


@authenticate.route('/api/login', methods=['POST', 'GET'], strict_slashes=False)
def api_login():
    """ check if email belongs to a user
            Failure: return error message
            Success: check is password is correct
                Failure: return error message
                Success: return user id
    """
    from models import User
    from main import auth
    # get login credentials
    email, pwd = request.form.get('email'), request.form.get('password')

    # check if email belongs to a user
    user = User.get_by_attr('email', email)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'invalid email'
        })

    # check if password is correct
    if not user.check_password(pwd):
        return jsonify({
            'status': 'error',
            'message': 'invalid password'
        })
    
    # user found, return user id and session id
    session = auth.begin_session(user.id)
    return jsonify({
        'status': 'success',
        'message': '',
        'userId': str(user.id),
        'session': session
    })