#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://qiita.com/orangain/items/6a166a65f5546df72a9d

from selenium.webdriver import Firefox, FirefoxOptions
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import time

# ヘッドレスモードオプション
options = FirefoxOptions()
options.add_argument('-headless')

# FirefoxのWebDriver作成
driver = Firefox(options=options)

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


