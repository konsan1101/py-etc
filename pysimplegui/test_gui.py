#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pysimplegui.readthedocs.io/en/latest/cookbook/

import PySimpleGUI as sg

# Very basic window.  Return values using auto numbered keys

layout = [
    [sg.Text(u'名前、住所、電話を入力してね。^^;')],
    [sg.Text(u'お名前', size=(15, 1)), sg.InputText()],
    [sg.Text(u'ご住所', size=(15, 1)), sg.InputText()],
    [sg.Text(u'電話番号', size=(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window(u'シンプル入力', layout)
event, values = window.Read()
window.Close()
print(event, values[0], values[1], values[2])    # the input data looks like a simple list when auto numbered
print(event, values)    


