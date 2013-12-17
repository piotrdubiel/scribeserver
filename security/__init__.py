from flask import Blueprint, make_response, jsonify, g
from flask.ext.httpauth import HTTPBasicAuth
from .models import User

blueprint = Blueprint('auth', __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_token(username_or_token)
    if not user:
        user = User.objects(email=username_or_token)[0]
        if not user.verify(password):
            return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

login_required = auth.login_required


@blueprint.route('/api/token')
@login_required
def token():
    return g.user.generate_token()

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return 'create'
