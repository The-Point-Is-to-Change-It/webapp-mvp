from flask import render_template
from main import auth
from blueprints.auth import authenticate


@authenticate.route('/register', methods=['GET'], strict_slashes=False)
def register():
    """
    Register a new user
    """
    return 'registering a user'


@authenticate.route('/login', methods=['GET'], strict_slashes=False)
def login():
    """
    Login a user
    """
    return 'login a user'


@authenticate.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """
    Logout a user
    """
    return 'logout a user'
