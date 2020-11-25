from api.v1 import api
from flask import jsonify, request


@api.route('/users/<limit>', methods=['GET'], strict_slashes=False)
@api.route('/users', methods=['GET'], strict_slashes=False)
def get_users(limit=None):
    """ get users from the db - if limit is provided, get that number """
    from models.storage import storage
    from models.users import User
    users = storage.get_all(User)
    if not limit:
        return jsonify(users)
    else:
        # this should be handled in the storage class in the future. look in to pagination with firestore
        limit = int(limit)
        ret = []
        for i in range(limit):
            ret.append(users[i])
        return jsonify(ret)