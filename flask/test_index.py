#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.sejuku.net/blog/55507

from flask import Flask, render_template
app = Flask(__name__)
 
@app.route('/')
def hello():
    #html = render_template('test_index.html')
    html = render_template('test_index.html', msg1='msg1', msg2='msg2', )

    #msg = {'msg1':u'あああ', 'msg2':u'いいい'}

    return html
 
if __name__ == "__main__":
    app.run()


