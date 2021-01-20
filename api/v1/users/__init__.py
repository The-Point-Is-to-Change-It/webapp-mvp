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

from api.v1 import api_v1, create_one_obj, get_all_or_n_obj
from flask import jsonify, request
from models.users import User



# POST /users - create a new user
def create_user():
    """
    create one new user/account
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
    # if all goes well so far, instantiate user
    if response.get('status') == 'OK':
        response['attributes']['email'] = email
        response['attributes']['password'] = password
        user = User(**response.get('attributes')).to_dict()
        del response['attributes']
        response['users'] = user
        del response['users']['password']
    return jsonify(response)


# GET /users - get all users
# GET /users/n - get some number of users
def get_all_or_n_users(n=None):
    """
    1. get all users or
    2. get some number of users
    """
    return jsonify(get_all_or_n_obj('User', n))
    

# DELETE /users/id - delete one user
def delete_user(id):
    user = User.get_n_by_cls_and_attr('id', id, 1)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'no user found'
        })
    User.delete_from_db_with_id(id)
    return jsonify({
        'status': 'OK',
        'message': 'user deleted',
        'users': user
    })


@api_v1.route('/users', methods=['POST', 'GET', 'DELETE'], strict_slashes=False)
@api_v1.route('/users/<int:n>', methods=['POST', 'GET', 'DELETE'], strict_slashes=False)
def user_post_get_delete(n=None):
    if request.method == 'POST':
        return create_user()
    elif request.method == 'GET':
        return get_all_or_n_users(n)
    elif request.method == 'DELETE':
        user_id = n
        return delete_user(user_id)

# GET /users/attr/value/ - get all users by attribute and value
# GET /users/attr/value/n - get n users by attribute and value (0 for all users)
@api_v1.route('users/<string:attr>/<value>', methods=['GET'], strict_slashes=False)
@api_v1.route('users/<string:attr>/<value>/<int:n>', methods=['GET'], strict_slashes=False)
def get_user_by_attr(attr, value, n=None):
    """
    1. get all users with att = value
    2. get n users with attr = value
    """
    if n:
        users = User.get_n_by_cls_and_attr(str(attr), str(value), n)
    else:
        users = User.get_all_by_cls_and_attr(str(attr), str(value))
    if not users or len(users) == 0:
        return jsonify({
            'status': 'error',
            'message': 'not found'
        }), 400
    return jsonify({
        'status': 'OK',
        'message': 'user(s) found',
        'users': users
    }), 200

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