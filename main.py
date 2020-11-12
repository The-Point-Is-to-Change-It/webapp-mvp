"""
-----------------------------
  The Point Is to Change It
-----------------------------

Responsive Webapp Entry Point
Contains:
1. bluprint registrations
2. authenticate request
3. error handling

"""

from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
from blueprints import authenticate
from blueprints import *


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
app.register_blueprint(home)
app.register_blueprint(authenticate)
app.register_blueprint(dash)

@app.before_request
def before():
    """
    Authenticate request
    """
    auth = Auth()
    auth.is_valid()
        



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


def build_url(endpoint):
    # in deployment
    # return 'http://thepointistochangeit.com/' + endpoint
    # in development
    return 'http://127.0.0.1:8080/' + endpoint


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
