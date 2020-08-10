#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response

import cv2
import time

import _v6_proc_camera
camera_thread = None
camDev = '0'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

    # "/" を呼び出したときには、indexが表示される。

def gen(camera_thread):
    #global camera_thread
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
    return Response(gen(camera_thread),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    if camera_thread is None:
        camera_thread = _v6_proc_camera.proc_camera(name='camera', id=camDev, runMode='debug', 
                        camDev=camDev, camMode='vga', camStretch='0', camRotate='0', camZoom='1.0', camFps='5',)
        camera_thread.begin()
        camDev = str(int(camDev) + 1)
        time.sleep(5)

    app.run(host='0.0.0.0', debug=True)

# 0.0.0.0はすべてのアクセスを受け付けます。    
# webブラウザーには、「localhost:5000」と入力