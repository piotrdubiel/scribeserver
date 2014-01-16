from flask import Blueprint, request
from tempfile import TemporaryFile
from users import api_authorize
from .models import Prediction
from PIL import Image

blueprint = Blueprint('recognition', __name__)

# ===============================================
#         ___  ____  __  ________________
#        / _ \/ __ \/ / / /_  __/ __/ __/
#       / , _/ /_/ / /_/ / / / / _/_\ \
#      /_/|_|\____/\____/ /_/ /___/___/
#
# ===============================================


@blueprint.route('/api/recognize', methods=['POST'])
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
