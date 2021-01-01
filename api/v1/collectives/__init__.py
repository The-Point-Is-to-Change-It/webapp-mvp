from flask import jsonify, request
from models import Collective
from api.v1 import api_v1




@api_v1.route('collectives/<limit>', methods=['GET'], strict_slashes=False)
@api_v1.route('collectives/', methods=['GET'], strict_slashes=False)
def get_collectives(limit=None):
    """
    get collectives from the db
    if limit is provided, get that number
    """
    from models.collectives import Collective

    # get a list of all collectives
    collectives = Collective.get_all()

    # all collectives are requested
    if not limit:
        return jsonify(collectives)
    else:
        # this should be handled in the storage class in the future. look into pagination with firestore
        limit = int(limit)
        ret = []
        if len(collectives) >= limit:
            for i in range(limit):
                ret.append(collectives[i])
        else:
            ret = {
                'status': 'error',
                'message': 'not enough collectives'
            }
        return jsonify(ret)

@api_v1.route('collectives/', methods=['POST'], strict_slashes=False)
def create_collective():
    """ return a new collective object with info from form """
    # get form data
    email, name = request.form.get('email'), request.form.get('name')
    handle = request.form.get('handle')

    # check all data is present
    if not email or not name or not handle:
        return jsonify(
            {'status': 'Error',
             'message': 'incomplete form'}
            ), 400
    
    # create new collective
    attrs = {
        'name': name,
        'email': email,
        'handle': handle,
        'profile_picture': '',
        'will': ''
    }

    # return json response
    return jsonify(Collective(**attrs).to_dict())
