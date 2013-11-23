#!/usr/bin/env python
from flask import Flask, request, Response
from flask.ext.pymongo import PyMongo
import json

app = Flask(__name__)
app.config.from_object('config.MongoConfig')

mongo = PyMongo(app)

@app.route('/register', methods=['POST'])
def register():
    token = generate_token()
    return token

@app.route('/train', methods=['POST'])
def train():
    import pdb; pdb.set_trace()  # XXX BREAKPOINT

    return Response('OK')

@app.route('/recognize', methods=['POST'])
def recognize():
    print("data : {}".format(request.form['data']))
    return "word"

if __name__ == '__main__':
    app.run(debug=True)
