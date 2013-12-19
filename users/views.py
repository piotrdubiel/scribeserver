from flask import Blueprint, jsonify, g, request, render_template, redirect, url_for
from .decorators import view_authorize, api_authorize

# ===============================================
#         ___  ____  __  ________________
#        / _ \/ __ \/ / / /_  __/ __/ __/
#       / , _/ /_/ / /_/ / / / / _/_\ \
#      /_/|_|\____/\____/ /_/ /___/___/
#
# ===============================================

blueprint = Blueprint('users', __name__)

@blueprint.route('/')
@view_authorize
def home():
    return render_template('index.html')

@blueprint.route('/api/token')
@api_authorize
def token():
    return g.user.generate_token()
