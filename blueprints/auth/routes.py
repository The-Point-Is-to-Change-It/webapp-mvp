from flask import render_template, make_response, redirect, request
from blueprints.auth import authenticate



@authenticate.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """
    POST request to /auth/api/register to register a new user
        Failure: redirect to landing page with error message
        Success: POST request to /auth/api/login to create a new session
            Failure: inform user of a server error
            Success: redirect to dashboard
    """
    import requests
    from main import build_url

    # use /auth/api/register endpoint to register user
    response = requests.post(build_url('auth/api/register'), data=request.form).json()
    
    # if registration fails, return an error message
    if response.get('status') == 'error':
        return render_template('/public/landing.html', error=response['message'])

    # user is registered, automatically log them in
    return redirect('/auth/login')


@authenticate.route('/login', methods=['GET'], strict_slashes=False)
def login():
    """
    Login a user if credentials are correct
    """
    import requests
    from main import build_url
    # if registration succeeds, user /auth/api/login endpoint to login
    response = requests.post(build_url('auth/api/login'), data=request.form).json()

    # set session cookie and redirect to dashboard
    ret = make_response(render_template('./dashboard.html'))
    ret.set_cookie('session', response.get('session'))
    return ret



@authenticate.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """
    Logout a user
    """
    return 'logout a user'
