#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response

import os
import time
import cv2

import _v6_proc_camera
camera_thread = None

app = Flask(__name__, static_folder='templates/static')
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    global camera_thread
    if camera_thread is None:
        camDev = '0'
        camera_thread = _v6_proc_camera.proc_camera(name='camera', id=camDev, runMode='debug', 
                        camDev=camDev, camMode='vga', camStretch='0', camRotate='0', camZoom='1.0', camFps='30',)
        camera_thread.begin()

    return render_template('index.html')

    # "/" を呼び出したときには、indexが表示される。

def gen():
    global camera_thread
    while True:
        hit = False
        while hit == False:
            res_data  = camera_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name == '[img]'):
                #cv2.imshow('Display', res_value.copy() )
                #cv2.waitKey(1)
                ret, jpeg = cv2.imencode('.jpg', res_value.copy())
                hit = True
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

# returnではなくジェネレーターのyieldで逐次出力。
# Generatorとして働くためにgenとの関数名にしている
# Content-Type（送り返すファイルの種類として）multipart/x-mixed-replace を利用。
# HTTP応答によりサーバーが任意のタイミングで複数の文書を返し、紙芝居的にレンダリングを切り替えさせるもの。
#（※以下に解説参照あり）

@app.route('/video_feed')
def video_feed():
    global camera_thread
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# アイコン
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )

# 0.0.0.0はすべてのアクセスを受け付けます。    
# webブラウザーには、「localhost:5000」と入力