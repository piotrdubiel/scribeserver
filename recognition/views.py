from flask import Blueprint, g, request
from users import api_authorize

blueprint = Blueprint('recognition', __name__)

# ===============================================
#         ___  ____  __  ________________
#        / _ \/ __ \/ / / /_  __/ __/ __/
#       / , _/ /_/ / /_/ / / / / _/_\ \
#      /_/|_|\____/\____/ /_/ /___/___/
#
# ===============================================


@blueprint.route('/api/recognize', methods=['POST'])
def recognize():
    print request.json
    return 'x'
