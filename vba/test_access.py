#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://code-life.hatenablog.com/entry/2018/05/15/PythonからExcelのVBA%EF%BC%88マクロ%EF%BC%89を実行する方法

# https://docs.microsoft.com/ja-jp/office/vba/api/access.application

import win32com.client  # ライブラリをインポート
import time

if __name__ == "__main__":

    access = win32com.client.Dispatch("Access.Application")
    access.OpenCurrentDatabase("C:/snkApps/SAAP_r545/近藤20200207SAAP2013R545_PGWK.accdb")
    access.Visible = True
    #access.Run "public_msg"
    time.sleep(10)
    access.UserControl = True
    #access.OpenCurrentDatabase()
    #access.Application.Quit()


