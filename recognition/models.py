from flask.ext.mongoengine import Document
import mongoengine as db


class Prediction(Document):
    image = db.ImageField()
    text = db.StringField()
