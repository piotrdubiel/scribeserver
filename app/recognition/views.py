from flask import Blueprint, request
from tempfile import TemporaryFile
from app.users import api_authorize
from .models import Prediction
from .cnn.classify import read
import struct
import os

blueprint = Blueprint('recognition', __name__)

from pysbp import Classifier
path = os.path.abspath(os.path.dirname(__file__))
classifier = Classifier(path + '/classifiers/pl_small_net.txt',
                        path + '/classifiers/pl_small_net.yml')


# ============================================= #
#         ___  ____  __  ________________       #
#        / _ \/ __ \/ / / /_  __/ __/ __/       #
#       / , _/ /_/ / /_/ / / / / _/_\ \         #
#      /_/|_|\____/\____/ /_/ /___/___/         #
#                                               #
# ============================================= #


@blueprint.route('/api/image/recognize', methods=['POST'])
@api_authorize
def image():
    print request.json
    with TemporaryFile(mode='wb+') as image_file:
        image_file.write(request.json['data'].decode('base64'))
        image_file.flush()
        image_file.seek(0, 0)

        prediction = Prediction(text='a')
        prediction.image.put(image_file, content_type="image/png")
        prediction.save()

    return 'a'


@blueprint.route('/api/recognize', methods=['POST'])
def gesture():
    a = read(request.json)
    return str(a)


@blueprint.route('/api/pca/recognize', methods=['POST'])
@api_authorize
def pca():
    vector = request.json['data'].decode('base64')
    values = list(struct.unpack('>' + 'f' * 150, vector))
    return classifier.classify(values)
