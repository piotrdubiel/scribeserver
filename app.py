#!/usr/bin/env python
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import MongoEngineUserDatastore

from users import User, Role, blueprint as users_module, security

app = Flask(__name__)
app.config.from_object('config.MongoConfig')
app.config['SECRET_KEY'] = '567633992e92e96c8a61f5e1ec62ba5550a9e95b4e2899a00112ebcd7585b1a9'

app.register_blueprint(users_module)

db = MongoEngine(app)
user_store = MongoEngineUserDatastore(db, User, Role)
security.init_app(app, user_store)

if __name__ == '__main__':
    app.run(debug=True)
