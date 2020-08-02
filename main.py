#!/usr/bin/env python3
"""
-------------------------------------------------------------------------------
Copyright (C) Russell Molimock - All Rights Reserved
Unauthorized copying of this application, via any medium is strictly prohibited
Proprietary and confidential
Written by Russell Molimock <admin@thepointistochangeit.com>, 2020
-------------------------------------------------------------------------------


-------------------------------
Flask App and Flask-login setup.
--------------------------------
"""
# this is the new one
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_cors import (CORS, cross_origin)
from flask import jsonify, Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from models.nav_link import *
from validate_email import validate_email

# from api.v1.views import app_views
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')



# instantiate the app, add cors protection, and check which authentication
# method it should run with.
app = Flask(__name__)
# app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
import secrets
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
print(app.secret_key)



"""
----------------------------
Flask-login setup
----------------------------
"""
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)
# login_manager.login_view = redirect on bad login


@login_manager.user_loader
def load_user(user_id):
    """
    Tell Flask-Login how to find a specific user
    from the ID that is stored in the session cookie.
    """
    return User.get(user_id)


"""
----------------------------
Authentication Routes
----------------------------
"""


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('indexx.html', nav_buttons=home_private_buttons)
    return render_template('indexx.html', nav_buttons=home_public_buttons)


@app.route('/profile')
@login_required
def profile():
    print(current_user.image)
    print(current_user.url)
    pub_user = current_user
    auth_user = None
    if current_user.is_authenticated:
        auth_user = current_user
        pub_user = None
    return render_template('profilex.html',
                            auth_user=auth_user,
                            pub_user=pub_user,
                            image=current_user.image,
                            nav_links=profile_private_links,
                            nav_buttons=profile_private_buttons)


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token=None):
    if request.method == 'GET':
        return render_template('auth/registerx.html',
                                nav_buttons=register_buttons,
                                GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)
    # post request
    image_url = None
    if token:
        print(token)
        guser = google_auth(request)
        if guser[0]:
            email = guser[1]['email']
            username = guser[1]['name']
            password = guser[1]['sub']
            image_url = guser[1]['picture']
            print(1)
        else:
            print(2)
            return guser[1]
    else:
        # get info from the registration form
        print(3)
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
    # check if the email is already in use
    print(4)
    if validate_email(username):
        flash('Username can not contain special characters.')
        print(5)
        return redirect('/')
    if not validate_email(email):
        flash('Email must be valid.')
        print(6)
        return redirect('/')
    # check if the password is strong enough
    if not password_check(password)[0] and not token:
        password_error = ''
        for k,v in password_check(password)[1].items():
            if v:
                password_error += k
        flash(password_error)
        print(7)
        return redirect('/')
    existing_user = User.search({'email': email})
    if existing_user:
        print('Email is already in use.')
        print(8)
        flash('Email is already in use.')
        return redirect(url_for('login'))
    # check the format of profile picture
    if not image_url:
        response = bad_uploaded_file(request)
        if response:
            print('file not ok')
            # flash happens in bad_uploaded_file()
            print(9)
            return redirect('/')
    user_info = {
                'email': email,
                'password': generate_password_hash(password, method='sha256'),
                'username': username
                }
    user = User(**user_info)
    if not image_url:
        print('no image! Whaaaaaa!?')
        file = request.files['file']
        save_profile_picture(file, user)
    else:
        print('imageurl:', image_url)
        user.image = image_url
    print('user image set to: ', user.image)
    print('user url set to ', user.url)
    user.save_to_db()
    flash(f'Welcome {username}!')
    login_user(user)
    print(10)
    return redirect(url_for('profile'))



def google_auth(request):
    token = request.form.getlist('idtoken')[0]
    from google.oauth2 import id_token
    from google.auth.transport import requests
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        userid = idinfo['sub']
    except ValueError:
        # Invalid token
        print('flase')
        return False
    if not idinfo['aud'] == GOOGLE_CLIENT_ID:
        flash('Inauthentic Google Sign In')
        return (False, redirect('register'))
    else:
        return (True, idinfo)


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/<token>', methods=['GET', 'POST'])
def login(token=None):
    if request.method == 'GET':
        return render_template('auth/loginx.html',
                                nav_buttons=login_buttons,
                                GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)
    # POST request
    if token:
        print(token)
        guser = google_auth(request)
        if guser[0]:
            username_or_email = guser[1]['email']
            password = guser[1]['sub']
            remember = True
            print(1)
        else:
            print(2)
            return guser[1]
    else:
        # get info from the registration form
        print(3)
        username_or_email = request.form.get('userNameOrEmail')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
    if validate_email(username_or_email):
        user = User.search({'email': username_or_email})
    else:
        user = User.search({'username': username_or_email})
    user = user[0] if user else None
    if not user:
        flash('No such email or username. \nPlease Register.')
        print(4)
        return redirect(url_for('register'))
    if not check_password_hash(user.password, str(password)):
        flash('Incorrect password.')
        print(5)
        return redirect(url_for('index'))
    login_user(user)
    return redirect(url_for('profile', remember=remember))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))








"""
----------------------------
Helper functions.
----------------------------
"""


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp']


def allowed_file(filename):
    # .split('.')[-1:][0]
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def bad_uploaded_file(request, file=None):
    if 'file' not in request.files:
        print(1)
        flash('Profile picture required.')
        return True
    file = request.files['file']
    if file.filename == '' or not '.' in file.filename:
        print(2)
        flash('Profile picture required.')
        return True
    if not allowed_file(file.filename):
        print(3)
        print(file.filename.split('.')[-1:][0])
        flash('Profile picture must be one of these formats: .png, .jpg, .jpeg, or .bmp')
        return True
    return False


def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the incorrect criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """
    import re
    # checking the length
    length_error = len(password) < 8
    # searching for digits
    digit_error = re.search(r"\d", password) is None
    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None
    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None
    # searching for symbols
    symbol_error = re.search(r"\W", password) is None
    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )
    return (password_ok,
            {
            'Password must contain: ': 1,
            'at least 8 characters, ' : length_error,
            'a number, ' : digit_error,
            'an uppercase letter, ' : uppercase_error,
            'a lowercase letter, ' : lowercase_error,
            'a symbol.' : symbol_error,
            })


def username_check(password):
    """
    Verify format of 'username'
    Returns a dict indicating the incorrect criteria
    A username is considered acceptable if:
        33 characters length or more
        no symbols or spaces
    """
    import re
    # checking the length
    length_error = len(password) > 33
    # searching for symbols
    symbol_error = re.search(r"\W", password)
    # overall result
    password_ok = not ( length_error or symbol_error )
    return (password_ok,
            {
            'Username must: be unique, ': 1,
            'be 33 characters or less, ' : length_error,
            'contain only text and/or numbers.' : symbol_error,
            })


def save_profile_picture(file, user):
    if file and allowed_file(file.filename):
        ext = secure_filename(file.filename).split('.')[-1:][0].lower()
        filename = user.id + '.' + ext
        file.save(os.path.join(os.path.dirname(__file__) + os.path.join(f"/static/images/users", filename)))
        user.image += ext
        user.save_to_db()


"""
----------------------------
Status checks
----------------------------
"""


@app.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    ----------------------------
    Check the status of the API.
    ----------------------------
    -> Return: Json response with status message "OK"
    """
    return jsonify({"status": "OK"})


"""
----------------------------
Error responses
----------------------------
"""


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def Forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def Unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    # set host and port #s based on environmental variables and run app
    host = os.getenv("API_HOST", "127.0.0.1")
    port = os.getenv("API_PORT", "8080")
    app.run(host=host, port=port)

