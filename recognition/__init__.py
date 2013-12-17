from flask import Blueprint, g
from security import login_required

blueprint = Blueprint('recognition', __name__)

@blueprint.route('/api/recognize')
@login_required
def recognize():
    return 'x'
