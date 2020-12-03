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


tmp_col = {
    'name': 'Collective Name',
    'handle': '@handle',
    'description': 'Description goes here.'
}
tmp_role = {
    'name': 'Role Name',
    'handle': '@handle',
    'description': 'Description goes here.'
}
tmp_auth = {
    'date': '1-01-2021',
    'action': 'action',
    'granted_to': 'Collective X'
}
tmp_post = {
    'content': 'This is a public post I made.',
    'upvotes': '7',
    'downvotes': '3'
}
tmp_prop = {
    'date': '1-01-2021',
    'description': 'I propose we do this and that.',
    'status': 'pending',
    'pass_condition': '50% + 1',
    'requirement': '5',
    'upvotes': '3',
    'downvotes': '1'
}
tmp_task = {
    'date': '1-01-2021',
    'status': 'incomplete',
    'description': 'Description of the task here.',
    'assigned_by': 'Role Y of Collective X'
}
tmp_dues = {
    'amount': '10',
    'frequency': 'monthly',
    'collective': 'Collective X'
}
context = {
    'task': tmp_task,
    'prop': tmp_prop,
    'post': tmp_post,
    'auth': tmp_auth,
    'role': tmp_role,
    'col': tmp_col,
    'dues': tmp_dues
}

@users.route('/collectives')
def collectives():
    """ view of my collectives widget """
    context['widget'] = 'col'
    return render_template('/dash/widget.html', context=context)

@users.route('/roles')
def roles():
    """ view of my roles widget """
    context['widget'] = 'role'
    return render_template('/dash/widget.html', context=context)

@users.route('/posts')
def posts():
    """ view of my public posts widget """
    context['widget'] = 'post'
    return render_template('/dash/widget.html', context=context)

@users.route('/tasks')
def tasks():
    """ view of my tasks widget """
    context['widget'] = 'task'
    return render_template('/dash/widget.html', context=context)

@users.route('/dues')
def dues():
    """ view of my dues widget """
    context['widget'] = 'dues'
    return render_template('/dash/widget.html', context=context)

@users.route('/proposals')
def proposals():
    """ view of my proposals widget """
    context['widget'] = 'prop'
    return render_template('/dash/widget.html', context=context)

@users.route('/authorities')
def authorities():
    """ view of my collectives widget """
    context['widget'] = 'auth'
    return render_template('/dash/widget.html', context=context)


"""
Other users
"""
@users.route('/<id>', methods=['GET'], strict_slashes=False)
def profile():
    """ public user profile """
    # from models.user import User
    # user = User.get_by_attr('id', id)
    return render_template('/dash/profile.html', user=id)