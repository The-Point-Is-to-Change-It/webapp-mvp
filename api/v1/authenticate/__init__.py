from api.v1 import api_v1
from flask import jsonify, request


# LOGIN - Create a session
@api_v1.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ create a session to log in """
    from models.auth.session import Session
    from models.users import User
    print(1)
    # get form data
    email, password = request.form.get('email'), request.form.get('password')
    response = {
        'status': 'error',
        'message': 'incomplete form'
        }
    print(2)

    # check all data is present
    if not email or not password:
        return jsonify(response), 400
    print(3)
    
    # validate user credentials
    user = User.get_n_by_cls_and_attr('email', email, 1)
    if not user or not user.get('password') == password:
        print(1)
        response['message'] = 'incorrect user credentials'
        return jsonify(response), 404
    print(4)
    
    # start a session
    session = Session(**{
        'user_id': user.get('id')
        })

    session_id = session.id
    del session
    # set cookie with session id
    return jsonify(
            {'id': session_id,
             'status': 'OK',
             'message': 'login successful',
             'user': user}
            ), 200



# AUTHENTICATE REQUEST - Update session
""" THIS IS NOT IN USE YET... NEEDS TO BE FIXED UP, NOT REQUEST.FORM, COOKIE, DUH! """
@api_v1.route('/sessions', methods=['PUT'], strict_slashes=False)
def authenticate_request():
    """ authenticate a request and update current session """
    from models.auth.session import Session
    from datetime import datetime

    # get session id passed in a cookie
    session = request.form.get('session')

    # check if it matches existing session, and ensure not expired
    if not session in Session.sessions or Session.sessions[session].expired():
        if Session.sessions[session].expired():
            del Session.sessions[session]
        # return error message if invalid or expired
        return jsonify(
            {'status': 'error',
             'message': 'session invalid or expired'}
            ), 404
    else:
        # update timestamp of session
        Session.sessions[session].created_at = datetime.utcnow()
        return jsonify(
            {'status': 'OK',
             'message': 'session updated',
             'user_id': Session.sessions[session].user_id
            }
        )


@api_v1.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ delete current session """
    from flask import make_response
    from models.auth.session import Session
    
    cookie = request.form.get('session')   
    if not cookie in Session.sessions:
        ret = jsonify(
            {'status': 'OK',
             'message': 'no session to delete',
            }
        )
    else:
        del Session.sessions[cookie]
        ret = jsonify(
            {'status': 'OK',
             'message': 'session deleted',
            }
        )
    bad_session_dict = Session.get_by_cls_and_attr('id', cookie)
    Session.delete_from_db_with_dict(bad_session_dict)
    print('session should be deleted')
    return ret
