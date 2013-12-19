from flask.ext.mongoengine import Document
from flask.ext.security import UserMixin, RoleMixin, passwordless
from passlib.apps import custom_app_context as pwd_context
import mongoengine as db


class Role(Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(Document, UserMixin):
    email = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    def hash(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify(self, password):
        return password == self.password_hash

    def generate_token(self, expiration=600):
        return passwordless.generate_login_token(self)

    @staticmethod
    def verify_token(token):
        return passwordless.login_token_status(token)[2]
