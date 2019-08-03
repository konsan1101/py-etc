#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pysimplegui.readthedocs.io/en/latest/cookbook/

import PySimpleGUI as sg

# Very basic window.  Return values using auto numbered keys

layout = [
    [sg.Text('Mode Radio', font=('Helvetica', 15), justification='left')],      
    [sg.Radio('Cross-Entropy', 'loss', size=(12, 1)), sg.Radio('Logistic', 'loss', default=True, size=(12, 1))],      
    [sg.Radio('Hinge', 'loss', size=(12, 1)), sg.Radio('Huber', 'loss', size=(12, 1))],      
    [sg.Radio('Kullerback', 'loss', size=(12, 1)), sg.Radio('MAE(L1)', 'loss', size=(12, 1))],      
    [sg.Radio('MSE(L2)', 'loss', size=(12, 1)), sg.Radio('MB(L0)', 'loss', size=(12, 1))], 
    [sg.Text('_'  * 100, size=(65, 1))],  

    [sg.Text('Option Flags', font=('Helvetica', 15), justification='left')],      
    [sg.Checkbox('Normalize', size=(12, 1), default=True), sg.Checkbox('Verbose', size=(20, 1))],      
    [sg.Checkbox('Cluster', size=(12, 1)), sg.Checkbox('Flush Output', size=(20, 1), default=True)],      
    [sg.Checkbox('Write Results', size=(12, 1)), sg.Checkbox('Keep Intermediate Data', size=(20, 1))],      
    [sg.Text('_'  * 100, size=(65, 1))],  

    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Simple data entry window', layout)
event, values = window.Read()
window.Close()
print(event, values[0], values[1], values[2])    # the input data looks like a simple list when auto numbered
print(event, values)    


