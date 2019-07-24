#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://qiita.com/orangain/items/6a166a65f5546df72a9d
#https://www.seleniumqref.com/api/webdriver_gyaku.html

from selenium.webdriver import Firefox, FirefoxOptions
import sys
import time

url='https://www.a-zip.co.jp/'
img='test_firefox.png'

if __name__ == '__main__':
    if (len(sys.argv) >= 2):
        url = str(sys.argv[1])
    if (len(sys.argv) >= 3):
        img = str(sys.argv[2])

    # ヘッドレスモードオプション
    options = FirefoxOptions()
    options.add_argument('-headless')

    # FirefoxのWebDriver作成
    driver = Firefox(options=options)

    # ウィンドウサイズとズームを設定
    driver.set_window_size(1920, 9999)
    driver.execute_script("document.body.style.zoom='100%'")

    # URLを開く
    driver.get(url)

    # 読み込み待機
    time.sleep(5)

    # webページショット
    #driver.get_screenshot_as_file(img)
    driver.save_screenshot(img)

    # プラウザを閉じる
    driver.quit()


