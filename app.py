#!/usr/bin/env python
from flask import Flask, render_template, Response, jsonify
from client import generate_token
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin, login_required

app = Flask(__name__)
app.config.from_object('config.MongoConfig')
app.config['SECRET_KEY'] = '567633992e92e96c8a61f5e1ec62ba5550a9e95b4e2899a00112ebcd7585b1a9'

db = MongoEngine(app)

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(email='matt@nobien.net', password='password')

@app.route('/')
@login_required
def hello():
    return Response('Hello')

@app.route('/register', methods=['POST'])
def register():
    return jsonify(token=generate_token())

@app.route('/train', methods=['POST'])
def train():
    return Response('OK')

@app.route('/recognize', methods=['POST'])
def recognize():
    print("data : {}".format(request.form['data']))
    return "word"

if __name__ == '__main__':
    app.run(debug=True)
