from flask import jsonify, request
from models import Collective
from api.v1 import (api_v1,
                    create_one_obj,
                    get_all_or_n_obj,
                    get_all_or_n_obj_by_attr,
                    update_object_attr_by_id,
                    remove_value_from_obj_attr,
                    delete_obj_from_db_with_id)


# POST /collectives - create a new collective
def create_collective():
    """
    route:
        POST /collectives
    1. verify data is present and handle is unique
    2. add the current user (creator of collective) to membership
    3. instantiate the collective
    4. return jsonified response
    Return -> dict: status, message, and new collective
    """
    # verify data is present and handle is unique
    response = create_one_obj('Collective')
    if response.get('status') == 'error':
        return jsonify(response)
    # add the current user (creator of collective) to membership
    if request.current_user:
        response['attributes']['members'] = [request.current_user]
    # instantiate collective
    collective = Collective(**response.get('attributes')).to_dict()
    response['collectives'] = collective
    # return jsonified response
    return jsonify(response)


# GET /collectives - get all collectives
# GET /collectives/n - get some number of collectives
def get_all_or_n_collectives(n=None):
    """
    routes:
        GET /collectives
        GET /collectives/n
    1. get all collectives or
    2. get some number of collectives
    Return -> dict: status, message, and new collective(s)
    """
    return jsonify(get_all_or_n_obj('Collective', n))

# GET /collectives/attr/value
# GET /collectives/attr/value/i
def get_all_or_n_collectives_by_attr(attr, value, i=None):
    """
    routes:
        GET /collectives/attr/value
        GET /collectives/attr/value/i
    1. get all collectives with attr = value or
    2. get some number of collectives with attr = value
    Return -> dict: status, message, and new collective(s)
    """
    return jsonify(get_all_or_n_obj_by_attr('Collective', attr, value, i))

def update_collective_attr_by_id(id, attr, value):
    """
    routes:
        PUT /collectives/id/attr/value
    1. update collective with attr = value or add value into attr if iterable
    Return -> dict: status, message, and updated collective
    """
    return jsonify(update_object_attr_by_id('Collective', id, attr, value))

def remove_value_from_collective_attr(id, attr, value):
    """
    routes:
        DELETE /collectives/id/attr/value
    1. remove value from attr or delete attr value entirely
    Return -> dict: status, message
    """
    return jsonify(remove_value_from_obj_attr('Collective', id, attr, value))

def delete_collective_by_id(id):
    """
    routes:
        DELETE /users/id
    1. delete user
    Return -> dict: status, message
    """
    print('in delete collective')
    return jsonify(delete_obj_from_db_with_id('Collective', id))


@api_v1.route('/collectives', methods=['POST', 'GET', 'DELETE'], strict_slashes=False)
@api_v1.route('/collectives/<n>', methods=['POST', 'GET', 'DELETE'], strict_slashes=False)
@api_v1.route('collectives/<string:attr>/<value>', methods=['GET'], strict_slashes=False)
@api_v1.route('collectives/<id>/<string:attr>/<value>', methods=['PUT', 'DELETE'], strict_slashes=False)
@api_v1.route('collectives/<string:attr>/<value>/<int:i>', methods=['GET'], strict_slashes=False)
def collective_routes(n=None, id=None, attr=None, value=None, i=None):
    if request.method == 'POST':
        return create_collective()
    elif request.method == 'GET':
        # /collectives
        # /collectives/n
        if not attr and not value and not i:
            return get_all_or_n_collectives(n)
        if attr and value:
            return get_all_or_n_collectives_by_attr(attr, value, i)
    elif request.method == 'PUT':
        return update_collective_attr_by_id(id, attr, value)
    elif request.method == 'DELETE':
        if id and attr and value:
            return remove_value_from_collective_attr(id, attr, value)
        collective_id = n
        return delete_collective_by_id(collective_id)


