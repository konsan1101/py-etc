#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pysimplegui.readthedocs.io/en/latest/cookbook/

import PySimpleGUI as sg
#import PySimpleGUIWeb as sg

# Very basic window.  Return values using auto numbered keys

layout = [
    # ＡＰＩ選択 free, google, watson, azure, nict, special
    [sg.Frame(layout=[
                       [sg.Radio('free', 'API', default=True), sg.Radio('google', 'API', key='google'), sg.Radio('watson', 'API'), 
                        sg.Radio('azure', 'API'), sg.Radio('nict', 'API'), sg.Radio('special', 'API')]
                    ], title=u'ＡＰＩ選択'),
    ],

    # モード選択 hud, live, translator, speech, number, camera, assistant
    [sg.Frame(layout=[
                       [sg.Radio('hud', 'MODE', default=True), sg.Radio('live', 'MODE'), sg.Radio('translator', 'MODE'), 
                        sg.Radio('speech', 'MODE'), sg.Radio('number', 'MODE'), sg.Radio('camera', 'MODE'), sg.Radio('assistant', 'MODE')]
                     ], title=u'モード選択'),
    ],

    [
        # speech
        sg.Frame(layout=[
                         [sg.Checkbox('main_speech', default=True)],
                         [sg.Checkbox('controls', default=True)],
                         [sg.Checkbox('adintool', default=True)],
                         [sg.Checkbox('voice2wav', default=True)],
                         [sg.Checkbox('coreSTT', default=True)],
                         [sg.Checkbox('coreTTS', default=True)],
                         [sg.Checkbox('playvoice', default=True)],
                         [sg.Checkbox('julius', default=True)],
                         [sg.Checkbox('sttreader', default=True)],
                         [sg.Checkbox('trareader', default=True)],
                         [sg.Text('')],
                         [sg.Text('')],
                         [sg.Text('')],
                      ], title=u'speech 起動条件'),
        # vision
        sg.Frame(layout=[
                         [sg.Checkbox('main_vision', default=True)],
                         [sg.Checkbox('controlv', default=True)],
                         [sg.Checkbox('overlay', default=True)],
                         [sg.Checkbox('camera1', default=True)],
                         [sg.Checkbox('camera2', default=True)],
                         [sg.Checkbox('txt2img', default=True)],
                         [sg.Checkbox('cvreader', default=True)],
                         [sg.Checkbox('cvdetect1', default=True)],
                         [sg.Checkbox('cvdetect2', default=True)],
                         [sg.Checkbox('cv2dnn_yolo', default=True)],
                         [sg.Checkbox('cv2dnn_ssd', default=True)],
                         [sg.Checkbox('vin2jpg', default=True)],
                         [sg.Checkbox('coreCV', default=True)],
                      ], title=u'vision 起動条件'),
        # desktop
        sg.Frame(layout=[
                         [sg.Checkbox('main_desktop', default=True)],
                         [sg.Checkbox('controld', default=True)],
                         [sg.Checkbox('capture', default=True)],
                         [sg.Checkbox('cvreader', default=True)],
                         [sg.Checkbox('recorder', default=True)],
                         [sg.Checkbox('uploader', default=True)],
                         [sg.Text('')],
                         [sg.Text('')],
                         [sg.Text('')],
                         [sg.Text('')],
                         [sg.Text('')],
                         [sg.Text('')],
                         [sg.Text('')],
                      ], title=u'desktop 起動条件'),
    ],

    [sg.Button(u'ＯＫ'), sg.Button(u'キャンセル')]
]

window = sg.Window(u'RiKi 設定入力', layout)
#window.Element('google').Update(1)

event, values = window.Read()
window.Close()
print(event, values[0], values[1], values[2])    # the input data looks like a simple list when auto numbered
print(event, values)    



