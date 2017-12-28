from flask import abort, request

from google.appengine.api import users

from swap import models
from swap.restutils import gen_error, gen_ok


def login_required(function):
    def login_required_wrapper(*args, **kw):
        if not users.get_current_user():
            return abort(401)
            # return redirect(users.create_login_url(request.path))
        return function(*args, **kw)
    return login_required_wrapper


@login_required
def item():
    if request.method == "POST":
        description = request.data
        if not description:
            return abort(400)
        result = models.Item(
            description=request.data,
            owner_id=users.get_current_user().user_id(),
            owner_email=users.get_current_user().email()
        )
        result.put()
        return gen_ok(result.key.id())
    else:  # GET
        owner = request.args.get(
            'owner', default=users.get_current_user().user_id(), type=str)
        result = models.Item.get_by_owner(owner)
    return gen_ok(result)


def swapping():
    data = request.get_json(force=True)
    if not data:
        return abort(400)

    try:
        my_item = int(data['my'])
        other_item = int(data['other'])
    except ValueError:
        return abort(400)

    if not models.Item.exists(my_item) or \
       not models.Item.exists(other_item) or \
       not models.Item.owned_by(my_item, users.get_current_user().user_id()):
        return abort(400)
    models.Item.swap(my_item, other_item)

    return gen_ok()


def error_404(e):
    error, code, headers = gen_error(message='Endpoint not found', code=404)
    return error, code, headers


def error_405(*args, **kwargs):
    error, code, headers = gen_error(message='Method not allowed', code=405)
    return error, code, headers


def error_500(e):
    error, code, headers = gen_error(
        message='Server is running in problems, contact'
        'rinat.sabitov@gmail.com if problem persists',
        code=500)
    return error, code, headers
