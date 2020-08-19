#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, Response, send_file, make_response

import os
import time
import datetime
import cv2
import io

import _v5_proc_capture
app_thread = None
app_seq    = 0

#app = Flask(__name__, template_folder='html', static_folder='html/static')
#app.config['JSON_AS_ASCII'] = False
#app.config['SECRET_KEY'] = os.urandom(24)
app = Blueprint('capture', __name__, template_folder='html', static_folder='html/static')

# ホーム
@app.route('/capture/')
def index():
    global app_thread
    if (app_thread is None):
        app_thread = _v5_proc_capture.proc_capture(name='capture', id='0', runMode='debug', 
                                                   capStretch='0', capRotate='0', capZoom='1.0', capFps='2', )
        app_thread.begin()

    return Response('''
    ホーム <br />
    <hr />
    <a href='/capture/stream/'>ストリーム表示</a> <br />
    <a href='/capture/interval/'>インターバル表示</a> <br />
    ''')

# ストリーム
@app.route('/capture/stream/')
def stream():
    return render_template('/capture/stream.html', filename='/capture/stream/result/image')

# フレーム取得
def frame():
    global app_thread
    while (True):
        hit = False
        while (hit == False):
            res_data  = app_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name == '[img]'):
                #cv2.imshow('Display', res_value.copy() )
                #cv2.waitKey(1)
                ret, jpeg = cv2.imencode('.jpg', res_value.copy())
                hit = True
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

# ストリーム応答
@app.route('/capture/stream/result/<name>')
def stream_result(name=None):
    return Response(frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# 1画像
@app.route('/capture/interval/')
def interval():
    global app_seq
    app_seq += 1
    if (app_seq > 9999):
        app_seq = 1
    seq4 = '{:04}'.format(app_seq)

    nowTime  = datetime.datetime.now()
    filename = nowTime.strftime('%Y%m%d.%H%M%S') + '.' + seq4 + '.jpg'

    return render_template('/capture/interval.html', filename='/capture/interval/result/' + filename)

# 1画像応答
@app.route('/capture/interval/result/<name>')
def interval_result(name=None):
    global app_thread
    hit = False
    while (hit == False):
        res_data  = app_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name == '[img]'):
            ret, jpeg = cv2.imencode('.jpg', res_value.copy())
            hit = True
    return send_file(io.BytesIO(jpeg), mimetype='image/jpeg', )

# アイコン
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


