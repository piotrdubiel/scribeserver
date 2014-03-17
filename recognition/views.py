from flask import Blueprint, request
from tempfile import TemporaryFile
from users import api_authorize
from .models import Prediction

blueprint = Blueprint('recognition', __name__)

import pysbp

# ===============================================
#         ___  ____  __  ________________
#        / _ \/ __ \/ / / /_  __/ __/ __/
#       / , _/ /_/ / /_/ / / / / _/_\ \
#      /_/|_|\____/\____/ /_/ /___/___/
#
# ===============================================


@blueprint.route('/api/image/recognize', methods=['POST'])
@api_authorize
def recognize():
    print request.json
    with TemporaryFile(mode='wb+') as image_file:
        image_file.write(request.json['data'].decode('base64'))
        image_file.flush()
        image_file.seek(0, 0)

        prediction = Prediction(text='a')
        prediction.image.put(image_file, content_type="image/png")
        prediction.save()

    return 'a'

@blueprint.route('/api/pca/recognize', methods=['POST'])
@api_authorize
def recognize():
    print request.json
    vector = request.json['data'].decode('base64')
    print vector
    return 'a'


@blueprint.route('/api/xor', methods=['GET'])
def xor():
    pysbp.init()
    pysbp.add_layer([43.259, 43.268, -66.366], [65.075, 65.101, -27.079])
    pysbp.add_layer([-29.041, 27.2972, -5.0622])

    return str(pysbp.classify(map(float, request.args.getlist('x'))))
