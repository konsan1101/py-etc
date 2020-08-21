#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, Response, send_file, make_response

import os
import time
import datetime

import io

import _v5_proc_voice2wav
app_thread = None
app_seq    = 0

import _v5_proc_adintool
app_thread2 = None
app_seq2    = 0



# ルート
route='/adin2wav'

if __name__ == '__main__':
    app = Flask(__name__, template_folder='html', static_folder='html/static')
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
else:
    app = Blueprint(route, __name__, template_folder='html', static_folder='html/static')



# ホーム
@app.route(route + '/')
def index():
    global app_thread, app_thread2
    if (app_thread is None):
        app_thread = _v5_proc_voice2wav.proc_voice2wav(name='voice2wav', id='0', runMode='debug',)
        app_thread.begin()
        app_thread2 = _v5_proc_adintool.proc_adintool(name='adintool', id='0', runMode='debug',)
        app_thread2.begin()

    return render_template(route + '/_index.html')

# プレイバック
@app.route(route + '/playback/')
def playback():
    global app_seq
    app_seq += 1
    if (app_seq > 9999):
        app_seq = 1
    seq4 = '{:04}'.format(app_seq)

    nowTime  = datetime.datetime.now()
    filename = nowTime.strftime('%Y%m%d.%H%M%S') + '.' + seq4 + '.wav'

    return render_template(route + '/playback.html', filename=route + '/playback/result/' + filename)

# 1応答
@app.route(route + '/playback/result/<name>')
def interval_result(name=None):
    global app_thread
    # 応答
    hit = False
    while (hit == False):
        res_data  = app_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name == 'filename'):
            wave = None
            try:
                rb = open(res_value, 'rb')
                wave = rb.read()
                rb.close
                rb = None
                hit = True
            except Exception as e:
                rb = None
        elif (res_name != ''):
            print(res_name, res_value, )
        time.sleep(0.01)
    return send_file(io.BytesIO(wave), mimetype='sound/wav', )

# アイコン
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, )


