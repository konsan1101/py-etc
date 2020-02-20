

import PySimpleGUI as sg
import vlc
import os

#------- GUI definition & setup --------#

sg.theme('Black')
sg.set_options(element_padding=(0,0), margins=(1,1), border_width=0)

def btn(name):  # a PySimpleGUI "User Defined Element" (see docs)
    return sg.Button(name, size=(6, 1), pad=(1, 1))

red_x = "R0lGODlhEAAQAPeQAIsAAI0AAI4AAI8AAJIAAJUAAJQCApkAAJoAAJ4AAJkJCaAAAKYAAKcAAKcCAKcDA6cGAKgAAKsAAKsCAKwAAK0AAK8AAK4CAK8DAqUJAKULAKwLALAAALEAALIAALMAALMDALQAALUAALYAALcEALoAALsAALsCALwAAL8AALkJAL4NAL8NAKoTAKwbAbEQALMVAL0QAL0RAKsREaodHbkQELMsALg2ALk3ALs+ALE2FbgpKbA1Nbc1Nb44N8AAAMIWAMsvAMUgDMcxAKVABb9NBbVJErFYEq1iMrtoMr5kP8BKAMFLAMxKANBBANFCANJFANFEB9JKAMFcANFZANZcANpfAMJUEMZVEc5hAM5pAMluBdRsANR8AM9YOrdERMpIQs1UVMR5WNt8X8VgYMdlZcxtYtx4YNF/btp9eraNf9qXXNCCZsyLeNSLd8SSecySf82kd9qqc9uBgdyBgd+EhN6JgtSIiNuJieGHhOGLg+GKhOKamty1ste4sNO+ueenp+inp+HHrebGrefKuOPTzejWzera1O7b1vLb2/bl4vTu7fbw7ffx7vnz8f///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJAALAAAAAAQABAAAAjUACEJHEiwYEEABniQKfNFgQCDkATQwAMokEU+PQgUFDAjjR09e/LUmUNnh8aBCcCgUeRmzBkzie6EeQBAoAAMXuA8ciRGCaJHfXzUMCAQgYooWN48anTokR8dQk4sELggBhQrU9Q8evSHiJQgLCIIfMDCSZUjhbYuQkLFCRAMAiOQGGLE0CNBcZYmaRIDLqQFGF60eTRoSxc5jwjhACFWIAgMLtgUocJFy5orL0IQRHAiQgsbRZYswbEhBIiCCH6EiJAhAwQMKU5DjHCi9gnZEHMTDAgAOw=="
layout = [
          [sg.Button('', image_data=red_x, key='-exit-', button_color=('black', 'black'), tooltip='Closes'),sg.Text('Mini Player')],
          [sg.Image('', size=(320, 240), key='-VID_OUT-')],
          [btn('previous'), btn('play'), btn('next'), btn('pause'), btn('stop')],
          [sg.Text('Load media to start', key='-MESSAGE_AREA-')]]

window = sg.Window('Mini Player', layout, 
                            keep_on_top=True,
                            no_titlebar=True,
                            alpha_channel=0.7,
                            finalize=True)

#------------ Media Player Setup ---------#

inst = vlc.Instance("--audio-visual=visual --effect-list=spectrum")
list_player = inst.media_list_player_new()
media_list = inst.media_list_new([])
list_player.set_media_list(media_list)
player = list_player.get_media_player()
if (os.name == 'nt'):
    player.set_hwnd(window['-VID_OUT-'].Widget.winfo_id())
else:
    player.set_xwindow(window['-VID_OUT-'].Widget.winfo_id())
#mac player.set_nsobject(window['-VID_OUT-'].Widget.winfo_id())

#media_list.add_media("C:/Users/Public/_m4v__Clip/GB/1edm.m4a")
media_list.add_media("C:/Users/Public/_m4v__Clip/GB")
#media_list.add_media("C:/Users/Public/_m4v__Clip/etc/Aerosmith_I Don't Want To Miss A Thing.mp4")
list_player.set_media_list(media_list)

#------------ The Event Loop ------------#
while True:
    event, values = window.read(timeout=1000)
    if (event in (None, '-exit-', '-cancel-')):
        break

    if event == 'play':
        player.audio_set_volume(100)
        list_player.play()
    if event == 'pause':
        list_player.pause()
    if event == 'stop':
        list_player.stop()
    if event == 'next':
        list_player.next()
        list_player.play()
    if event == 'previous':
        list_player.previous()      # first call causes current video to start over
        list_player.previous()      # second call moves back 1 video from current
        player.audio_set_volume(100)
        list_player.play()

    # update elapsed time if there is a video loaded and the player is playing
    if player.is_playing():
        window['-MESSAGE_AREA-'].update("{:02d}:{:02d} / {:02d}:{:02d}".format(*divmod(player.get_time()//1000, 60),
                                                                     *divmod(player.get_length()//1000, 60)))
    else:
        window['-MESSAGE_AREA-'].update('Load media to start' if media_list.count() == 0 else 'Ready to play media' )

window.close()
