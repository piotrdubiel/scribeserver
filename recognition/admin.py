from flask.ext.admin.contrib.mongoengine import ModelView
from .models import Prediction
from admin import AdminMixin


class PredictionView(AdminMixin, ModelView):
    column_searchable_list = ('text',)