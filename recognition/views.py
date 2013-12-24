from flask import Blueprint, g, request
from users import api_authorize

blueprint = Blueprint('recognition', __name__)


@blueprint.route('/api/recognize')
@api_authorize
def recognize():
    print request.json
    return 'x'
