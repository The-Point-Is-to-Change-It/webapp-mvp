"""
-----------------------------
  The Point Is to Change It | API
-----------------------------

API Contains:
1. all api endpoints to be accessed by the app or (sometimes) client

"""

from flask import Blueprint, render_template, jsonify


api_v1 = Blueprint("api", __name__, url_prefix="/api")


@api_v1.route('/', methods=['GET'], strict_slashes=False)
def index():
    return jsonify({'Status': 'OK'}), 200

