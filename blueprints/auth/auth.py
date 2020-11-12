"""
-----------------------------
  The Point Is to Change It - Auth
-----------------------------

Contained in auth.py:
1. Auth Class Definition

"""

from flask import request, abort
from blueprints.auth import authenticate


class Auth():
    """
    1. registration
    2. session-based authentication
    3. logout (destroy session)
    """

    sessions = {}
    session_timeout = 200

    def __init__(self):
        """
        Initiate an instance
        """
        from uuid import uuid4
        self.id = str(uuid4())
    
    def begin_session(self, user_id):
        """
        Create and store a token associated with user_id
        """
        new_session = self.id
        Auth.sessions[new_session] = user_id
        return new_session

    def is_public(self, route: str) -> bool:
        """
        Check if a route or endpoint is accessible to the current user
        Return: True if allowed, otherwise False
        """

        public_routes = ['/', '/auth/*', '/static/*']
        print(route)
        for proute in public_routes:
            if proute.endswith('*') and route.startswith(proute[:-1]):
                return True
            if route == proute:
                return True
        return False

    def is_valid(self):
        """
        Authenticate a request
        Check if page requested is public, if not check session cookie
            Failure: abort
            Success: do nothing
        """
        # put if not logged in
        # user not authenticated and path is private
        if not self.is_public(request.path):
            if not request.cookies.get('session'):
                abort(401)
            

auth = Auth()
auth.begin_session('email')
