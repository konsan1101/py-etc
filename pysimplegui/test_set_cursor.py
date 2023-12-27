
#- 'arrow' : 矢印
#- 'circle' : 円
#- 'cross' : 十字
#- 'hand' : 手
#- 'question' : 質問符
#- 'size_ns' : 上下の矢印
#- 'size_we' : 左右の矢印
#- 'watch' : 時計

import PySimpleGUI as sg
layout = [[sg.Button('Change Cursor')]]
window = sg.Window('Cursor Example', layout)

toggle = False

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Change Cursor':
        if toggle == False:
            window.set_cursor('watch')
            toggle = True
        elif toggle != False:
            window.set_cursor('arrow')
            toggle = False

window.close()
