#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.sejuku.net/blog/55507

from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False // <-- これ
 
@app.route('/', methods=['GET', 'POST'])
def index():
    msg = 'Hello world!'
    return msg
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )

