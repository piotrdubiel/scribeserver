from flask import Blueprint, g
from users import api_authorize

blueprint = Blueprint('recognition', __name__)


@blueprint.route('/api/recognize')
@api_authorize
def recognize():
    return 'x'
