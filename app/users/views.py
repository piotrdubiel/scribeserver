from flask import Blueprint, jsonify, g, request, render_template, redirect, url_for
from flask.ext.login import current_user
from flask.ext.security import RegisterForm
from flask.ext.security.registerable import register_user
from flask.ext.security.utils import login_user
from werkzeug.datastructures import MultiDict
from .decorators import view_authorize, api_authorize, http_authorize

blueprint = Blueprint('users', __name__)

# ===============================================
#         ___  ____  __  ________________
#        / _ \/ __ \/ / / /_  __/ __/ __/
#       / , _/ /_/ / /_/ / / / / _/_\ \
#      /_/|_|\____/\____/ /_/ /___/___/
#
# ===============================================

@blueprint.route('/')
@view_authorize
def home():
    return render_template('index.html')

@blueprint.route('/api/token', methods=['POST'])
@http_authorize
def token():
    return current_user.get_auth_token()

@blueprint.route('/api/register', methods=['POST'])
def register():
    form_data = MultiDict(request.json)
    form = RegisterForm(form_data)
    user = register_user(**form.to_dict())
    login_user(user)
    return current_user.get_auth_token()
