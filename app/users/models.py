from flask.ext.mongoengine import Document
from flask.ext.security import UserMixin, RoleMixin
import mongoengine as db


class Role(Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class Device(Document):
    name = db.StringField(max_length=127)
    identifier = db.StringField(max_length=255)
    active = db.BooleanField(default=True)


class User(Document, UserMixin):
    email = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    devices = db.ListField(db.ReferenceField(Device), default=[])
