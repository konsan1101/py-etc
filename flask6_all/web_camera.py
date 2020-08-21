#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, Response, send_file, make_response

import os
import time
import datetime
import cv2
import io

import _v5_proc_camera
app_thread = None
app_seq    = 0



# ルート
route='/camera'

if __name__ == '__main__':
    app = Flask(__name__, template_folder='html', static_folder='html/static')
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
else:
    app = Blueprint(route, __name__, template_folder='html', static_folder='html/static')



# ホーム
@app.route(route + '/')
def index():
    global app_thread
    if (app_thread is None):
        camDev = '0'
        app_thread = _v5_proc_camera.proc_camera(name='camera', id=camDev, runMode='debug', 
                                                 camDev=camDev, camMode='vga', camStretch='0', camRotate='0', camZoom='1.0', camFps='30',)
        app_thread.begin()

    return render_template(route + '/_index.html')

# ストリーム
@app.route(route + '/stream/')
def stream():
    return render_template(route + '/stream.html', filename=route + '/stream/result/image')

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
            elif (res_name != ''):
                print(res_name, res_value, )
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

# ストリーム応答
@app.route(route + '/stream/result/<name>')
def stream_result(name=None):
    return Response(frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# 1画像
@app.route(route + '/interval/')
def interval():
    global app_seq
    app_seq += 1
    if (app_seq > 9999):
        app_seq = 1
    seq4 = '{:04}'.format(app_seq)

    nowTime  = datetime.datetime.now()
    filename = nowTime.strftime('%Y%m%d.%H%M%S') + '.' + seq4 + '.jpg'

    return render_template(route + '/interval.html', filename=route + '/interval/result/' + filename)

# 1画像応答
@app.route(route + '/interval/result/<name>')
def interval_result(name=None):
    global app_thread
    # 1枚目スキップ
    hit = False
    while (hit == False):
        res_data  = app_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name == '[img]'):
            hit = True
        elif (res_name != ''):
            print(res_name, res_value, )
    # 2枚目有効
    hit = False
    while (hit == False):
        res_data  = app_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name == '[img]'):
            ret, jpeg = cv2.imencode('.jpg', res_value.copy())
            hit = True
        elif (res_name != ''):
            print(res_name, res_value, )
    return send_file(io.BytesIO(jpeg), mimetype='image/jpeg', )

# アイコン
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


