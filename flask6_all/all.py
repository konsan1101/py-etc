#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, Response, send_file, make_response

import os
import time
import datetime

app = Flask(__name__, template_folder='html', static_folder='html/static')
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)

import camera
app.register_blueprint(camera.app)

import capture
app.register_blueprint(capture.app)

import recorder
app.register_blueprint(recorder.app)

# ホーム
@app.route('/')
def index():
    return Response('''
    ホーム <br />
    <hr />
    <a href='/camera/'>カメラ表示</a> <br />
    <a href='/capture/'>キャプチャ表示</a> <br />
    <a href='/recorder/'>録画制御</a> <br />
    ''')

# アイコン
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


