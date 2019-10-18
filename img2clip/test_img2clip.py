#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://water2litter.net/rum/post/python_win32clipboard_set/

import tkinter
import tkinter.ttk
from PIL import Image, ImageTk
import win32clipboard
import io

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('clipboard trial')
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # ボタン
        self.original_button = tkinter.ttk.Button(self, text='Copy to Clipboard')
        self.original_button.grid(row=0, column=1)
        self.original_button.bind('<Button-1>', copy_to_clipboard)

        # canvas
        self.test_canvas = tkinter.Canvas(self, width=original_image.width, height=original_image.height)
        self.test_canvas.grid(row=0, column=0)

        # canvasに初期画像を表示
        self.test_canvas.photo = ImageTk.PhotoImage(original_image)
        self.image_on_canvas = self.test_canvas.create_image(0, 0, anchor='nw', image=self.test_canvas.photo)

def copy_to_clipboard(event):
    # メモリストリームにBMP形式で保存してから読み出す
    output = io.BytesIO()
    original_image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)

def send_to_clipboard(clip_type, data):
    # クリップボードをクリアして、データをセットする
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

# 画像ファイル読み込み
original_image = Image.open('dog.jpg')

# アプリケーション起動
root = tkinter.Tk()
app = Application(master=root)
app.mainloop()


