#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, session, render_template
import os

import cv2
import time

app_count    = 0
video_enable = False

app = Flask(__name__, static_folder='templates/static')
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET', 'POST'], )
def root():
    global app_count, video_enable, video
    if (video_enable != True):
        video = cv2.VideoCapture(0)
        success, image = video.read()
    return 'VideoCapture started! cam=../cam, '

@app.route('/cam', methods=['GET', 'POST'], )
def cam():
    global app_count, video_enable, video
    success, image = video.read()
    app_count += 1
    filename = 'result_' + str(app_count) + '.jpg'
    cv2.imwrite('templates/static/images/' + filename, image)
    time.sleep(1)
    return render_template('view.html', filename=filename)
    
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


