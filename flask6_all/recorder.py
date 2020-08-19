#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, Response, send_file, make_response

import os
import time
import datetime
import cv2
import io

import _v5_proc_recorder
app_thread = None
app_seq    = 0

#app = Flask(__name__, template_folder='html', static_folder='html/static')
#app.config['JSON_AS_ASCII'] = False
#app.config['SECRET_KEY'] = os.urandom(24)
app = Blueprint('recorder', __name__, template_folder='html', static_folder='html/static')

# ホーム
@app.route('/recorder/')
def index():
    global app_thread
    if (app_thread is None):
        camDev = '0'
        app_thread = _v5_proc_recorder.proc_recorder(name='recorder', id='0', runMode='debug',)
        app_thread.begin()

    return Response('''
    ホーム <br />
    <hr />
    <a href='/recorder/start/'>録画開始</a> <br />
    <a href='/recorder/abort/'>録画終了</a> <br />
    ''')

# 録画開始
@app.route('/recorder/start/')
def start():
    global app_thread
    app_thread.put(['control', u'録画開始'])
    return Response('''
    録画開始 <br />
    <hr />
    <a href='/recorder/'>ホーム</a> <br />
    ''')
    return

# 録画終了
@app.route('/recorder/abort/')
def abort():
    global app_thread
    app_thread.put(['control', u'録画終了'])
    return Response('''
    録画終了 <br />
    <hr />
    <a href='/recorder/'>ホーム</a> <br />
    ''')
    return

# アイコン
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


