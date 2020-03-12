#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://code-life.hatenablog.com/entry/2018/05/15/PythonからExcelのVBA%EF%BC%88マクロ%EF%BC%89を実行する方法

import win32com.client  # ライブラリをインポート
import time

if __name__ == "__main__":

    excel = win32com.client.Dispatch("Excel.Application")  # インスタンス生成
    excel.Visible = 1  # エクセルを表示する設定（0にすれば非表示で実行される）
    excel.Workbooks.Open(Filename="C:/Users/kondou/Documents/GitHub/py-etc/vba/test_excel.xlsm", ReadOnly=1)  # ブックを読み取り専用で開く
    excel.Application.Run('public_msg')  # マクロ名を指定して実行（引数なしの場合マクロ名のみで実行可能）
    excel.Workbooks(1).Close(SaveChanges=1)  # ブックを保存して閉じる（SaveChangesを0にすると保存せず閉じる）
    #time.sleep(10)
    excel.Application.Quit()  # 終了    app.run()


