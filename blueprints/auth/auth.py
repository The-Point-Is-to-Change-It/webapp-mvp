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

    def validate(self):
        """
        Authenticate a request
        """
        # put if not logged in
        # user not authenticated and path is private
        if not self.is_public(request.path):
            abort(401)
            

auth = Auth()

