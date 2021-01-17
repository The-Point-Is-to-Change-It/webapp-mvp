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
        return jsonify({
            'status': 'OK',
            'message': 'all collectives',
            'collectives': collectives
        })
    else:
        # this should be handled in the storage class in the future. look into pagination with firestore
        limit = int(limit)
        limited_collectives = []
        if len(collectives) >= limit:
            for i in range(limit):
                limited_collectives.append(collectives[i])
            response = jsonify({
                'status': 'OK',
                'message': 'all collectives',
                'collectives': limited_collectives
            })
        else:
            response = jsonify({
                'status': 'error',
                'message': 'not enough collectives',
                'collectives': collectives
            })
        return response

@api_v1.route('collectives/', methods=['POST'], strict_slashes=False)
def create_collective():
    """ return a new collective object with info from form """
    # ALSO ADD CURRENT USER TO MEMBERSHIP!
    # get form data
    name = request.form.get('name')
    handle = request.form.get('handle')

    # check all data is present
    if not name or not handle:
        return jsonify(
            {'status': 'Error',
             'message': 'incomplete form'}
            ), 400
    
    # create new collective
    attrs = {
        'name': name,
        'handle': handle,
        'profile_picture': '',
        'will': ''
    }

    # return json response
    return jsonify(Collective(**attrs).to_dict())



# GET /collectives/attr/value/ - get all collectives by attribute and value
# GET /collectives/attr/value/n - get n collectives by attribute and value (0 for all collectives)
@api_v1.route('collectives/<string:attr>/<value>', methods=['GET'], strict_slashes=False)
@api_v1.route('collectives/<string:attr>/<value>/<int:n>', methods=['GET'], strict_slashes=False)
def get_collective_by_attr(attr, value, n=None):
    """
    1. get all collectives with att = value
    2. get n collectives with attr = value
    """
    if n:
        collectives = Collective.get_n_by_cls_and_attr(str(attr), str(value), n)
    else:
        collectives = Collective.get_all_by_cls_and_attr(str(attr), str(value))
    if n == 1:
            collectives = collectives[0]
    if not collectives or len(collectives) == 0:
        return jsonify({
            'status': 'error',
            'message': 'not found'
        }), 400
    return jsonify({
        'status': 'OK',
        'message': 'collective(s) found',
        'collectives': collectives
    }), 200
