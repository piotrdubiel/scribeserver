from flask.ext.mongoengine import Document
from flask.ext.security import passwordless
from passlib.apps import custom_app_context as pwd_context
import mongoengine as db


class Role(Document):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(Document):
    email = db.StringField(max_length=255)
    password_hash = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    def hash(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify(self, password):
        return password == self.password_hash
        #return pwd_context.verify(password, self.password_hash)

    def generate_token(self, expiration=600):
        return passwordless.generate_login_token(self)

    @staticmethod
    def verify_token(username_or_token):
        return passwordless.login_token_status(username_or_token)[2]
