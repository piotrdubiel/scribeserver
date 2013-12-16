from flask import Blueprint, g
from auth import login_required

api = Blueprint('api', __name__)


@api.route('/api/token')
@login_required
def token():
    return g.user.generate_token()


@api.route('/api/recognize')
@login_required
def recognize():
    return 'x'
