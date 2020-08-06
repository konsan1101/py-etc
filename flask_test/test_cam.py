#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, session, render_template
import os

import cv2

video_enable = False


app = Flask(__name__, static_folder='templates/static')
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET', 'POST'], )
def root():
    global video_enable,video
    if (video_enable != True):
        video = cv2.VideoCapture(0)
    return 'VideoCapture started! cam=../cam, '

@app.route('/cam', methods=['GET', 'POST'], )
def cam():
    global video_enable,video
    success, image = video.read()
    cv2.imwrite('templates/static/images/capture.jpg', image)

    return render_template('view.html')
    
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("images/favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


