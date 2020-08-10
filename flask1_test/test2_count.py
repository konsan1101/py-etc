#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.rithmschool.com/courses/intermediate-flask/cookies-sessions-flask

from flask import Flask, session
#import random
import os

a=0

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#app.config['SECRET_KEY'] = str(random.random())
app.config['SECRET_KEY'] = os.urandom(24)

@app.before_request
def before_request():
    print('before_request')

@app.teardown_request
def teardown_request(exception):
    print('teardown_request')

@app.route('/', methods=['GET', 'POST'], )
def root():
    session['count'] = 0
    return 'New counter started! count=../count, clear=../clear, '

@app.route('/count', methods=['GET', 'POST'], )
def count():
    global a
    if not isinstance(session.get('count'), int):
        return 'No counter set!'

    session['count'] += 1
    a += 1
    return str(session['count']) + ', ' + str(a)
    
@app.route('/clear', methods=['GET', 'POST'], )
def clear_count():
    session.pop('count', None)
    return 'Counter cleared!'

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


