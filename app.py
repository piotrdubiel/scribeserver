#!/usr/bin/env python
from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/recognize', methods=['POST'])
def convert():
    print("data : {}".format(request.form['data']))
    return "hello " + request.form['id'] + " " +request.form['data']

if __name__ == '__main__':
    app.run(debug=True)
