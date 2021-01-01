from flask import abort, request

class Auth():
    @classmethod
    def authenticate(cls, url):
        """ parent method of Auth class, all others called from here """
        route = Auth.get_route(url)
        if not route:
            abort(400)
        # check if route is public, private, or neither
        is_public = Auth.public_route(route)
        is_private = Auth.private_route(route)
        # check if session cookie exists and is valid, if so set current user
        authenticated_user = Auth.current_user(request.cookies.get('session'))
        return Auth.set_view(is_public, is_private, authenticated_user)

    @classmethod
    def get_route(cls, url):
        """
        format the request url to isolate the route
        """
        if url.startswith('http://127.0.0.1'):
            return url[21:]
        if not url.startswith('https'):
            return None
        elif url.startswith('https://thepointistochangeit.com'):
            return url[32:]
        else:
            return None

    @classmethod
    def public_route(cls, route):
        """
        check if path is fully public such as the landing page
        """
        if route == '/' or route.startswith('/api') or route.startswith('/static'):
            return True
        return False

    @classmethod
    def private_route(cls, route):
        """
        check if page requested has a private version
        such as a user or collective profile
        """
        if route.startswith('/collectives') or route.startswith('/users') or route == '/notifications':
            return True
        return False

    @classmethod
    def current_user(cls, cookie):
        """
        check for a session cookie, if it matches an existing
        one, and if it's expired
        """
        from models.auth.session import Session
        from datetime import datetime
        if not cookie:
            return None
        this_session_dict = Session.get_by_cls_and_attr('id', cookie)
        if not this_session_dict:
            return None
        if Session.expired(this_session_dict):
            return None
        Session.update_attr_by_id(cookie, 'created_at', datetime.utcnow())
        return this_session_dict['user_id']

    @classmethod
    def set_view(cls, is_public, is_private, authenticated_user):
        """
        set whether or not to load the full/privileged version of a template
        """
        # not signed in, viewing public page - show full landing page with register/login forms
        if is_public and not authenticated_user:
            full_view = True
        # signed in, viewing public page - show landing page without register/login form
        if is_public and authenticated_user:
            full_view = False
        # if not signed in, viewing private page - show only public version (user/collective public profile)
        if not authenticated_user and is_private:
            full_view = False
        # if signed in, viewing private page - potentially show user account/collective dashboard
        # CHECK PERMISSION IN THOSE ROUTES
        if authenticated_user and is_private:
            full_view = True
        # if not signed in, viewing pages neither public nor private
        if not authenticated_user and not is_private and not is_public:
            full_view = False
        # if signed in, viewing pages neither public nor private
        if authenticated_user and not is_private and not is_public:
            full_view = True
        return full_view, authenticated_user
