#!/usr/bin/env python
from flask import Flask, render_template, Response, jsonify
from flask.ext.mongoengine import MongoEngine

import recognition
import security

app = Flask(__name__)
app.config.from_object('config.MongoConfig')
app.config['SECRET_KEY'] = '567633992e92e96c8a61f5e1ec62ba5550a9e95b4e2899a00112ebcd7585b1a9'

app.register_blueprint(security.blueprint)
app.register_blueprint(recognition.blueprint)

db = MongoEngine(app)

if __name__ == '__main__':
    app.run(debug=True)
