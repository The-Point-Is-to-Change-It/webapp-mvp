"""
-----------------------------
  The Point Is to Change It | API
-----------------------------

API Contains:
1. all api endpoints to be accessed by the app or (sometimes) client

"""

from flask import Blueprint, render_template, jsonify, request


api_v1 = Blueprint("api", __name__, url_prefix="/api")

ALLOWED_CLASSES = ['User', 'Collective', 'Role', 'Will', 'Authority']

def get_all_or_n_obj(cls_name, n=None):
    """
    route: GET /cls_name
    """
    # response is OK by default
    response = {
                'status': 'OK',
                'message': f'{cls_name.lower()}s found'
        }
    # check that a valid model is being created
    if cls_name not in ALLOWED_CLASSES:
        response = {'status': 'error',
                    'message': 'no such class'}
    # import cls_name and get all objects
    if response.get('status') == 'OK':
        module_name = cls_name.lower() + 's'
        exec(f'from models.{module_name} import {cls_name}')
        print(f'{cls_name}.get_all_or_n_cls({n})')
        objects = eval(f'{cls_name}.get_all_or_n_cls({n})') or None
        if not objects:
            response = {'status': 'error',
                        'message': f'no {cls_name.lower()} found'}
        else:
            response[f'{cls_name.lower()}s'] = objects
    print(cls_name, n)
    print('response is ', response)
    return response
  

def create_one_obj(cls_name):
    """
    route: POST /cls_name
    Complete steps common to all object creation endpoints
    1. check that a valid model is being created
    2. check that all data is present
    3. check that handle is unique
    Return -> dict: status, message, and attributes for instantiation
    """
    # response is OK by default
    response = {'status': 'OK', 'message': f'{cls_name.lower()} created'}
    # check that a valid model is being created
    if cls_name not in ALLOWED_CLASSES:
        response = {'status': 'error',
                    'message': 'no such class'}
    # check that all data is present
    name, handle = request.form.get('name'), request.form.get('handle')
    if not name or not handle:
        response = {'status': 'error',
                    'message': 'incomplete form'}
    # import cls_name and check that handle is unique
    module_name = cls_name.lower() + 's'
    exec(f'from models.{module_name} import {cls_name}')
    if exec(f'{cls_name}.get_n_by_cls_and_attr("handle", "{handle}", 1)'):
        response = {'status': 'error',
                    'message': 'handle must be unique'}
    response['attributes'] = {
        'name': name,
        'handle': handle
    }
    # return status, message, and attributes (used to instantiate class)
    return response

@api_v1.route('/', methods=['GET'], strict_slashes=False)
def index():
    return jsonify({'Status': 'OK'}), 200

