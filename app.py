#!/usr/bin/env python
from flask import Flask, request, Response
from flask import jsonify
from client import generate_token

app = Flask(__name__)
app.config.from_object('config.MongoConfig')

@app.route('/')
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
