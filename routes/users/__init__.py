"""
-----------------------------
  The Point Is to Change It | Routes - users
-----------------------------

Routes - users Contains:
1. all routes for user userss and profile (public and private)
2. calls api endpoints to interact with db

"""

from flask import Blueprint, render_template

users = Blueprint("users", __name__, url_prefix="/users")


@users.route('/', methods=['GET'], strict_slashes=False)
def all():
    """ your users/profile page """
    return 'this will be a paginated list of all users to browse through'


@users.route('/me', methods=['GET'], strict_slashes=False)
def account():
    """ your users/profile page """
    return render_template('/dash/account.html')

"""
Individual widgets for user
"""
@users.route('/collectives')
def collectives():
    """ view of my collectives widget """
    return render_template('/dash/widget.html')

@users.route('/roles')
def roles():
    """ view of my roles widget """
    return render_template('/dash/widget.html')

@users.route('/posts')
def posts():
    """ view of my public posts widget """
    return render_template('/dash/widget.html')

@users.route('/tasks')
def tasks():
    """ view of my tasks widget """
    return render_template('/dash/widget.html')

@users.route('/dues')
def dues():
    """ view of my dues widget """
    return render_template('/dash/widget.html')

@users.route('/proposals')
def proposals():
    """ view of my proposals widget """
    return render_template('/dash/widget.html')

@users.route('/authorities')
def authorities():
    """ view of my collectives widget """
    return render_template('/dash/widget.html')


"""
Other users
"""
@users.route('/<id>', methods=['GET'], strict_slashes=False)
def profile():
    """ public user profile """
    # from models.user import User
    # user = User.get_by_attr('id', id)
    return render_template('/dash/profile.html', user=id)