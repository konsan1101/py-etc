#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response, send_file

import os
import time
import cv2
import io

import _v6_proc_camera
app_thread = None
app_seq    = 0

app = Flask(__name__, static_folder='templates/static')
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    global app_thread
    if (app_thread is None):
        camDev = '0'
        app_thread = _v6_proc_camera.proc_camera(name='camera', id=camDev, runMode='debug', 
                                                 camDev=camDev, camMode='vga', camStretch='0', camRotate='0', camZoom='1.0', camFps='30',)
        app_thread.begin()

    return Response('''
    ホーム <br />
    <hr />
    <a href='/stream/'>ストリーム表示</a> <br />
    <a href='/oneshot/'>ワンショット表示</a> <br />
    ''')

@app.route('/stream/')
def stream():
    return render_template('stream.html')

def gen():
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

@app.route('/stream_feed')
def stream_feed():
    global app_thread
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/oneshot/')
def oneshot():
    global app_thread, app_seq
    hit = False
    while (hit == False):
        res_data  = app_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name == '[img]'):
            ret, jpeg = cv2.imencode('.jpg', res_value.copy())
            hit = True
    #return (b'--frame\r\n'
    #    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    #return send_file(
    #    io.BytesIO(jpeg),
    #    mimetype='image/jpeg',
    #    as_attachment=True,
    #    attachment_filename=filename + '.jpg',
    #    )

    #response = make_response(jpeg)
    #response.headers.set('Content-Type', 'image/jpeg')
    #response.headers.set(
    #    'Content-Disposition', 'attachment', filename=filename + '.jpg')
    #return response

    app_seq += 1
    if (app_seq >= 10):
        app_seq = 1
    seq4 = '{:04}'.format(app_seq)
    filename = 'result_' + seq4 + '.jpg'
    cv2.imwrite('templates/static/images/' + filename, res_value)
    return render_template('oneshot.html', filename=filename)

# アイコン
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

# スタイル
@app.route("/destyle.css")
def destyle():
    return app.send_static_file("destyle.css")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


