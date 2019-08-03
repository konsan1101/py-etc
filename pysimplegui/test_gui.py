#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pysimplegui.readthedocs.io/en/latest/cookbook/

import PySimpleGUI as sg

# Very basic window.  Return values using auto numbered keys

layout = [
    [sg.Text('Please enter your Name, Address, Phone')],
    [sg.Text('Name', size=(15, 1)), sg.InputText()],
    [sg.Text('Address', size=(15, 1)), sg.InputText()],
    [sg.Text('Phone', size=(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Simple data entry window', layout)
event, values = window.Read()
window.Close()
print(event, values[0], values[1], values[2])    # the input data looks like a simple list when auto numbered
print(event, values)    


