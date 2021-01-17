"""
-----------------------------
  The Point Is to Change It | Entry Point
-----------------------------

Entry Point Contains:
1. bluprint registrations
2. authenticate request
3. error handling
4. global helper functions

"""

from flask import Flask, jsonify, request, json, abort, g
from flask_cors import (CORS, cross_origin)
from routes import *
from api import *
from os import environ
from uuid import uuid4
import requests


# initiate flask app and secret key
app = Flask(__name__)
if "FLASK_SECRET_KEY" in environ:
    app.secret_key = environ["FLASK_SECRET_KEY"]
else:
    environ["FLASK_SECRET_KEY"] = str(uuid4())

# cors protection
CORS(app, resources={r"*": {"origins": "*"}})

# register routes
app.register_blueprint(landing)
app.register_blueprint(dash)
app.register_blueprint(users)
app.register_blueprint(collectives)
app.register_blueprint(auth)

# register api endpoints
app.register_blueprint(api_v1)



@app.before_request
def before():
    """
    authenticate request before routes
    """
    from models.auth import Auth
    # isolate requested route from url
    request.full_view, request.current_user = Auth.authenticate(request.url)


@app.errorhandler(400)
def bad_request(error) -> str:
    """
    Request is bad
    """
    return jsonify({"error": "Bad Request, https required"}), 400


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def Forbidden(error) -> str:
    """
    Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def Unauthorized(error) -> str:
    """
    Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
