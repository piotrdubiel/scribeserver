from flask.ext.mongoengine import Document
import mongoengine as db

from users import Device


class Prediction(Document):
    image = db.ImageField()
    text = db.StringField()
    device = db.ReferenceField(Device)
