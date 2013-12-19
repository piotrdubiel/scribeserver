from flask import make_response, jsonify, g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.security import Security, login_required, auth_token_required
from .models import User

basic_auth = HTTPBasicAuth()
security = Security()


@basic_auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_token(username_or_token)
    if not user:
        user = User.objects(email=username_or_token)[0]
        if not user.verify(password):
            return False
    g.user = user
    return True


@basic_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


api_authorize = auth_token_required
view_authorize = login_required
