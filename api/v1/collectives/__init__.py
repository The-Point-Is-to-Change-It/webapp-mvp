from flask import jsonify, request
from models import Collective
from api.v1 import api_v1


# POST /collectives - create a new collectives
def create_collective():
    """
    create one new collective
    """
    # get form data
    name, handle = request.form.get('name'), request.form.get('handle')
    # check all data is present
    if not name or not handle:
        return jsonify(
            {'status': 'error',
             'message': 'incomplete form'}
            ), 400
    # check handle is unique
    if Collective.get_all_by_cls_and_attr('handle', handle):
        return jsonify(
            {'status': 'error',
             'message': 'email and handle must be unique'}
            ), 400
    # create new collectives
    attrs = {
        'name': name,
        'handle': handle
    }
    collective = Collective(**attrs).to_dict()
    return jsonify({
        'status': 'OK',
        'message': 'collective created',
        'collectives': collective
    })

# GET /collectives - get all collectives
# GET /collectives/n - get some number of collectives
def get_collectives(n=None):
    """
    1. get all collectives
    2. get some number of usecollectivesrs
    """
    collectives = Collective.get_all_or_n_cls(n)
    if collectives:
        return jsonify({
                'status': 'OK',
                'message': f'all collectives',
                'collectives': collectives
            }), 200
    return jsonify({
                'status': 'error',
                'message': f'no matching collectives',
            }), 400

# DELETE /collectives/id - delete one collective
def delete_collective(id):
    collective = Collective.get_n_by_cls_and_attr('id', id, 1)
    if not collective:
        return jsonify({
            'status': 'error',
            'message': 'no collective found'
        })
    Collective.delete_from_db_with_id(id)
    return jsonify({
        'status': 'OK',
        'message': 'collective deleted',
        'collectives': collective
    })


@api_v1.route('/collectives', methods=['POST', 'GET', 'DELETE'], strict_slashes=False)
@api_v1.route('/collectives/<int:n>', methods=['POST', 'GET', 'DELETE'], strict_slashes=False)
def collective(n=None):
    if request.method == 'POST':
        return create_collective()
    elif request.method == 'GET':
        return get_collectives(n)
    elif request.method == 'DELETE':
        collective_id = n
        return delete_collective(collective_id)



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
