#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome, ChromeOptions
import time

# ヘッドレスモードオプション
options = ChromeOptions()
options.add_argument('-headless')

# ChromeのWebDriver作成
driver = Chrome(options=options)

# URLを開く
driver.get('https://www.a-zip.co.jp/')

# 読み込み待機
time.sleep(5)

# ウィンドウサイズとズームを設定
driver.set_window_size(1280, 3000)
driver.execute_script("document.body.style.zoom='90%'")

# webページショット
driver.save_screenshot('test_azip.png')

# プラウザを閉じる
driver.quit()


