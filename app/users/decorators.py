from functools import wraps
from flask import request, current_app
from flask.ext.security import login_required, auth_token_required, http_auth_required
from flask.ext.security import utils


api_authorize = auth_token_required
http_authorize = http_auth_required
view_authorize = login_required


def json_authorize(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        security = current_app.extensions['security']
        if _check_json_auth():
            return fn(*args, **kwargs)
        else:
            return security._unauthorized_callback()
    return decorator


def _check_json_auth():
    security = current_app.extensions['security']
    auth = request.get_json()
    user = security.datastore.find_user(email=auth['email'])

    if user and utils.verify_and_update_password(auth['password'], user):
        utils.login_user(user)
        return True

    return False
