from flask.ext.mongoengine import Document
from flask.ext.security import UserMixin, RoleMixin
import mongoengine as db

class Prediction(Document):
    image = db.ImageField()
    text= db.StringField()

