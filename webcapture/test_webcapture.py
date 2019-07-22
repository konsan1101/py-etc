#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver

# プラウザ起動（Chrome）
driver = webdriver.Chrome

# ドメインの一部をファイル名として設定
site_name = "https://www.a-zip.co.jp/"
file_name = "test_azip.png"
# URLを開く
driver.get(site_name)
# ウィンドウサイズとズームを設定
driver.set_window_size(1280, 3000)
#driver.execute_script("document.body.style.zoom='90%'")
# 読み込み待機時間
time.sleep(5)
# imagesフォルダにスクリーンショットを保存
driver.save_screenshot(file_name)

# プラウザを閉じる
driver.quit()


