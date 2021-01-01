from api.v1 import api_v1
from flask import jsonify, request



# POST USERS
@api_v1.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    CREATE A NEW USER ACCOUNT
    """
    from models.users import User

    # get form data
    email, name = request.form.get('email'), request.form.get('name')
    handle, password = request.form.get('handle'), request.form.get('password')

    # check all data is present
    if not email or not name or not handle or not password:
        return jsonify(
            {'status': 'error',
             'message': 'incomplete form'}
            ), 400
    
    # check email and handle are unique and fields are valid
    print(User.get_by_cls_and_attr('email', email))
    
    # create new user
    attrs = {
        'name': name,
        'email': email,
        'handle': handle,
        'password': password
    }
    return jsonify(User(**attrs).to_dict())





@api_v1.route('/users/<limit>', methods=['GET'], strict_slashes=False)
@api_v1.route('/users', methods=['GET'], strict_slashes=False)
def get_users(limit=None):
    """ get users from the db - if limit is provided, get that number """
    from models.users import User
    users = User.get_all()
    if not limit:
        return jsonify(users)
    else:
        # this should be handled in the storage class in the future. look in to pagination with firestore
        limit = int(limit)
        ret = []
        for i in range(limit):
            ret.append(users[i])
        return jsonify(ret)


