#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pypi.org/project/PySimpleGUI/2.30.0/

import PySimpleGUI as sg



event = sg.Popup('Popup')
print(event)

event = sg.PopupOK('PopupOk')
print(event)

event = sg.PopupOKCancel('PopupOkCancel')
print(event)

event = sg.PopupYesNo('PopupYesNo')
print(event)

event = sg.PopupCancel('PopupCancel')
print(event)

event = sg.PopupError('PopupError')
print(event)

event = sg.PopupTimed('PopupTimed')
print(event)

event = sg.PopupAutoClose('PopupAutoClose')
print(event)    


