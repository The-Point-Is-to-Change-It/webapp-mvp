""""
Users module contains the following:


POST /users - create a new user

GET /users - get all users
GET /users/n - get some number of users
GET /users/attr/value/ - get all users by attribute and value - also check if attr is list or dict and value in attr instead of == attr
GET /users/attr/value/n - get n users by attribute and value (0 for all users)

UPDATE /users/id/attr/value - update one user with attr = value
UPDATE /users/attr/value - update all users with attr = value
UPDATE /users/id/invites/collective_id - invite user to join collective

DELETE /users/id - delete one user by id
DELETE /users/attr/value - delete all users with attr = value
DELETE /users/id/invites/collective_id - undo invitation to user to join collective

"""

from api.v1 import (api_v1,
                   create_one_obj,
                   get_all_or_n_obj,
                   get_all_or_n_obj_by_attr,
                   update_object_attr_by_id,
                   remove_value_from_obj_attr,
                   delete_obj_from_db_with_id)
from flask import jsonify, request
from models.users import User



def create_user():
    """
    route: POST /users
    1. verify data is present and handle is unique
    2. check that email and password are present
    3. check that email is unique
    4. instantiate the user
    5. return jsonified response
    Return -> dict: status, message, and new user
    """
    # verify data is present and handle is unique
    response = create_one_obj('User')
    if response.get('status') == 'error':
        return jsonify(response)
    # check that email and password are present
    email, password = request.form.get('email'), request.form.get('password')
    if not email or not password:
        response = {'status': 'error',
                    'message': 'incomplete form'}
    # check that email is unique
    if User.get_n_by_cls_and_attr('email', email, 1):
        response = {'status': 'error',
                    'message': 'email must be unique'}
    # if all goes well so far, instantiate the user
    if response.get('status') == 'OK':
        response['attributes']['email'] = email
        response['attributes']['password'] = password
        user = User(**response.get('attributes')).to_dict()
        del response['attributes']
        response['users'] = user
        del response['users']['password']
    # return jsonified response
    return jsonify(response)


# GET /users - get all users
# GET /users/n - get some number of users
def get_all_or_n_users(n=None):
    """
    1. get all users or
    2. get some number of users
    """
    return jsonify(get_all_or_n_obj('User', n))

# GET /users/attr/value
# GET /users/attr/value/i
def get_all_or_n_users_by_attr(attr, value, i=None):
    """
    routes:
        GET /users/attr/value
        GET /users/attr/value/i
    1. get all users with attr = value or
    2. get some number of users with attr = value
    Return -> dict: status, message, and new user(s)
    """
    return jsonify(get_all_or_n_obj_by_attr('User', attr, value, i))
    
def update_user_attr_by_id(id, attr, value):
    """
    routes:
        PUT /users/id/attr/value
    1. update user with attr = value or add value into attr if iterable
    Return -> dict: status, message, and updated user
    """
    return jsonify(update_object_attr_by_id('User', id, attr, value))

def remove_value_from_user_attr(id, attr, value):
    """
    routes:
        DELETE /users/id/attr/value
    1. remove value from attr or delete attr value entirely
    Return -> dict: status, message
    """
    return jsonify(remove_value_from_obj_attr('User', id, attr, value))

def delete_user_by_id(id):
    """
    routes:
        DELETE /users/id
    1. delete user
    Return -> dict: status, message
    """
    print('in delete user')
    return jsonify(delete_obj_from_db_with_id('User', id))
    


@api_v1.route('/users', methods=['POST', 'GET'], strict_slashes=False)
@api_v1.route('/users/<n>', methods=['POST', 'GET', 'DELETE'], strict_slashes=False)
@api_v1.route('users/<string:attr>/<value>', methods=['GET'], strict_slashes=False)
@api_v1.route('users/<id>/<string:attr>/<value>', methods=['PUT', 'DELETE'], strict_slashes=False)
@api_v1.route('users/<string:attr>/<value>/<int:i>', methods=['GET'], strict_slashes=False)
def user_routes(n=None, id=None, attr=None, value=None, i=None):
    if request.method == 'POST':
        return create_user()
    elif request.method == 'GET':
        # /users
        # /users/n
        if not attr and not value and not i:
            return get_all_or_n_users(n)
        # /users/attr/value
        # /users/attr/value/i
        if attr and value:
            print(attr, value)
            return get_all_or_n_users_by_attr(attr, value, i)
    elif request.method == 'PUT':
        return update_user_attr_by_id(id, attr, value)
    elif request.method == 'DELETE':
        if id and attr and value:
            print('found attr and value')
            return remove_value_from_user_attr(id, attr, value)
        else:
            user_id = n
            print(user_id)
            return delete_user_by_id(user_id)



'''
# UPDATE /users/id/attr/value - update one user with attr = value
@api_v1.route('/users/<id>/<attr>/<value>', methods=['UPDATE'], strict_slashes=False)
def update_one_user(id, attr, value):
    """
    find user by id and set their attr = value
    """
    user = User.get_n_by_cls_and_attr('id', id, 1)
    if not user or len(user) == 0:
        return jsonify({
            'status': 'error',
            'message': 'user not found'
        }), 400
    user = user[0]
    if 'attr' in user:
        User.update_attr_by_id(user.get('id'), attr, value)
    return jsonify({
            'status': 'OK',
            'message': 'user updated',
            'user': user
        }), 200


# UPDATE /users/attr/value - update all users with attr = value
@api_v1.route('/users/<attr>/<value>', methods=['UPDATE'], strict_slashes=False)
def update_users(attr, value):
    """
    update all users to have attr = value
    """
    return {'status': 'yo'}, 400
    users = User.get_all_by_cls_and_attr(attr, value)
    if not users or len(users) == 0:
        return jsonify({
            'status': 'error',
            'message': 'user not found'
        }), 400
    for user in users:
        user.update_attr_by_id(user.get('id'), attr, value)
    return jsonify({
        'status': 'OK',
        'message': 'users updated'
    })


# UPDATE /users/id/invites/collective_id - invite user to join collective
@api_v1.route('/users/<entity_id>/invites/<collective>', methods=['UPDATE'], strict_slashes=False)
def send_invite(entity_id, collective):
    """ invite an entity into the collective """
    return



"""



DELETE /users/id - delete one user by id
DELETE /users/attr/value - delete all users with attr = value
DELETE /users/id/invites/collective_id - undo invitation to user to join collective
"""
'''