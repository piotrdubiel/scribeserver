from flask.ext.admin.contrib.mongoengine import ModelView
from .models import Prediction
from app.management.mixins import AdminMixin


class PredictionView(AdminMixin, ModelView):
    column_searchable_list = ('text',)
