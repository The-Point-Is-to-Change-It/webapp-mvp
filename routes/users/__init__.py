"""
-----------------------------
  The Point Is to Change It | Routes - users
-----------------------------

Routes - users Contains:
1. all routes for user userss and profile (public and private)
2. calls api endpoints to interact with db

"""

from flask import Blueprint, render_template, request, redirect, url_for

users = Blueprint("users", __name__, url_prefix="/users")




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

@users.route('/', methods=['GET'], strict_slashes=False)
@users.route('/<id>', methods=['GET'], strict_slashes=False)
def profile(id=None):
    """ public user profile """
    from models.users import User
    # not logged in and entered /user
    if not request.current_user and not id:
        return redirect(url_for('landing.index'))
    # not logged in and viewing a user page
    if not request.current_user and id:
        user = User.get_n_by_cls_and_attr('id', id, 1)
        if not user:
            return redirect(url_for('dash.public_square'))
        data = {
            'user': user,
            'full_view': request.full_view
        }
        return render_template('/dash/public_profile.html', data=data)
    # logged in and viewing your account
    if request.current_user:
        if not id or id == request.current_user:
            user = User.get_n_by_cls_and_attr('id', request.current_user, 1)
            data = {
                'current_user': user,
                'full_view': request.full_view
            }
            return render_template('/dash/account.html', data=data)
    # logged in and viewing another user profile
    if request.current_user and id and not id == request.current_user:
        user = User.get_n_by_cls_and_attr('id', id, 1)
        current_user = User.get_n_by_cls_and_attr('id', request.current_user, 1)
        print('IN HERE YO')
        print(request.current_user)
        data = {
            'user': user,
            'current_user': current_user,
            'full_view': request.full_view
        }
        return render_template('/dash/public_profile.html', data=data)
    return redirect(url_for('landing.index'))

