from api.v1 import api
from flask import jsonify, request
from models import Collective


@api.route('/collectives/<limit>', methods=['GET'], strict_slashes=False)
@api.route('/collectives', methods=['GET'], strict_slashes=False)
def get_collectives(limit=None):
    """ get collectives from the db - if limit is provided, get that number """
    from models.storage import storage
    from models.collectives import Collective
    collectives = storage.get_all(Collective)
    if not limit:
        return jsonify(collectives)
    else:
        # this should be handled in the storage class in the future. look in to pagination with firestore
        limit = int(limit)
        ret = []
        for i in range(limit):
            ret.append(collectives[i])
        return jsonify(ret)

@api.route('/collectives', methods=['POST'], strict_slashes=False)
def create_collective():
    """ return a new collective object with info from form """
    email, username = request.form.get('email'), request.form.get('username')
    handle, password = request.form.get('handle'), request.form.get('password')
    if not email or not username or not handle:
        return jsonify(
            {'status': 'Error',
             'message': 'incomplete form'}
            ), 400
    attrs = {
        'username': username,
        'email': email,
        'handle': handle,
        'password': password
    }
    return Collective(**attrs).to_dict()
