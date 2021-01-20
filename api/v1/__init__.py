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

"""
POST METHODS --------------------------------------------------------
"""

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

"""
GET METHODS ---------------------------------------------------------
"""

def get_all_or_n_obj(cls_name, n=None):
    """
    route:
        GET /cls_name
        GET /cls_name/n
    Complete steps common to all get/get n object endpoints
    1. check that a valid model is being requested
    2. get all or n objects
    Return -> dict: status, message, found objects
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
        objects = eval(f'{cls_name}.get_all_or_n_cls({n})') or None
        if not objects:
            response = {'status': 'error',
                        'message': f'no {cls_name.lower()} found'}
        else:
            response[f'{cls_name.lower()}s'] = objects
    return response


def get_all_or_n_obj_by_attr(cls_name, attr, value, i=None):
    """
    route:
        GET /cls_name/attr/value
        GET /cls_name/attr/value/i
    Complete steps common to all get/get n by attribute object endpoints
    1. check that a valid model is being requested
    2. get all or n objects by attr = value
    Return -> dict: status, message, found objects
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
        print(f'{cls_name}.get_n_by_cls_and_attr("{attr}", "{value}", {i})')
        objects = eval(f'{cls_name}.get_n_by_cls_and_attr("{attr}", "{value}", {i})')
        if not objects:
            response = {'status': 'error',
                        'message': f'no {cls_name.lower()} found'}
        else:
            for obj in objects:
                print(obj.get('name'))
            response[f'{cls_name.lower()}s'] = objects
    return response

"""
PUT METHODS ---------------------------------------------------------
"""

def update_object_attr_by_id(cls_name, id, attr, value):
    """
    route:
        PUT /cls_name/id/attr/value
    Complete steps common to all put object endpoints
    1. check that a valid model is being created
    2. get object by id
    3. depending on attr, either set attr = value or add value to attr
    Return -> dict: status, message
    """
    # response is OK by default
    response = {
                'status': 'OK',
                'message': 'value updated'
        }
    # check that a valid model is being created
    if cls_name not in ALLOWED_CLASSES:
        response = {'status': 'error',
                    'message': 'no such class'}
    # import cls_name and get all objects
    if response.get('status') == 'OK':
        module_name = cls_name.lower() + 's'
        exec(f'from models.{module_name} import {cls_name}')
        eval(f'{cls_name}.update_attr_by_id("{id}", "{attr}", "{value}")')
    # object updated
    return response

"""
DELETE METHODS ------------------------------------------------------
"""

def delete_obj_from_db_with_id(cls_name, id):
    """
    route:
        DELETE /cls_name/id
    Complete steps common to all delete object endpoints
    1. check that a valid model is being deleted
    2. get object by id
    3. delete object
    Return -> dict: status, message
    """
    print('delete object from id')
    # response is OK by default
    response = {
                'status': 'OK',
                'message': f'{cls_name.lower()} deleted'
        }
    # check that a valid model is being created
    if cls_name not in ALLOWED_CLASSES:
        response = {'status': 'error',
                    'message': 'no such class'}
    # import cls_name and get all objects
    if response.get('status') == 'OK':
        module_name = cls_name.lower() + 's'
        exec(f'from models.{module_name} import {cls_name}')
        print(f'{cls_name}.delete_from_db_with_id("{id}")')
        eval(f'{cls_name}.delete_from_db_with_id("{id}")')
    # object deleted
    print('response', response)
    return response

def remove_value_from_obj_attr(cls_name, id, attr, value):
    """
    route:
        DELETE /cls_name/id/attr/value
    Complete steps common to all value deletion object endpoints
    1. check that a valid model is being created
    2. get object by id
    3. depending on attr, either delete entire value or remove it from attr
    Return -> dict: status, message
    """
    # response is OK by default
    response = {
                'status': 'OK',
                'message': 'value removed'
        }
    # check that a valid model is being created
    if cls_name not in ALLOWED_CLASSES:
        response = {'status': 'error',
                    'message': 'no such class'}
    # import cls_name and get all objects
    if response.get('status') == 'OK':
        module_name = cls_name.lower() + 's'
        exec(f'from models.{module_name} import {cls_name}')
        eval(f'{cls_name}.remove_attr_value("{id}", "{attr}", "{value}")')
    # object updated
    return response


@api_v1.route('/', methods=['GET'], strict_slashes=False)
def index():
    return jsonify({'Status': 'OK'}), 200

