#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, Response, send_file, make_response

import os
import time
import datetime



app = Flask(__name__, template_folder='html', static_folder='html/static')
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)

import web_camera
app.register_blueprint(web_camera.app)

import web_capture
app.register_blueprint(web_capture.app)

import web_recorder
app.register_blueprint(web_recorder.app)

import web_adin2wav
app.register_blueprint(web_adin2wav.app)


# ルート
route=''

# ホーム
@app.route(route + '/')
def index():
    return render_template(route + '/_index.html')

# アイコン
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


