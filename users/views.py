from flask import Blueprint, jsonify, g, request, render_template, redirect, url_for
from flask.ext.login import current_user
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

@blueprint.route('/api/token')
@http_authorize
def token():
    return current_user.get_auth_token()
