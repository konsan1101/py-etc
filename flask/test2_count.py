#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.rithmschool.com/courses/intermediate-flask/cookies-sessions-flask

from flask import Flask, session
import random

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # <-- これ
app.config['SECRET_KEY'] = random.random()

@app.route('/', methods=['GET', 'POST'], )
def root():
    session['count'] = 0
    return 'New counter started! count=../count, clear=../clear, '

@app.route('/count', methods=['GET', 'POST'], )
def count():
    count = session.get('count')
    if isinstance(count, int):
        session['count'] += 1
        return str(session['count'])
    return 'No counter set!'

@app.route('/clear', methods=['GET', 'POST'], )
def clear_count():
    session.pop('count', None)
    return 'Counter cleared!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


