#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://funmatu.wordpress.com/2017/06/01/pyautogui%EF%BC%9Fpywinauto%EF%BC%9F/

import os
import time
import numpy as np
import cv2

if (os.name == 'nt'):
    import win32gui
    import win32api
    import win32ui
    import win32con

    from PIL import Image
 
class win_shot_class:

    def __init__(self, ):
        #os.mkdir('temp')
        #os.mkdir('temp/_work')
        #self.workPath = 'temp/_work/'
        #self.proc_seq = 0
        pass

    def screenshot(self, ):
        #self.proc_seq += 1
        #if (self.proc_seq > 99):
        #    self.proc_seq = 1
        #seq2 = '{:02}'.format(self.proc_seq)
        #filename = self.workPath + 'screenshot.' + seq2 + '.bmp'

        try:

            SM_XVIRTUALSCREEN = 76
            SM_YVIRTUALSCREEN = 77
            SM_CXVIRTUALSCREEN = 78
            SM_CYVIRTUALSCREEN = 79
            w = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
            h = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
            l = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
            t = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
            
            hwnd = win32gui.GetDesktopWindow()
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
            saveDC.SelectObject(saveBitMap)
            saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (l, t),  win32con.SRCCOPY)

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
            return img

        except:
            return False

    def windowshot(self, ):

        try:

            SM_CXVIRTUALSCREEN = 78
            SM_CYVIRTUALSCREEN = 79
            full_w = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
            full_h = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)

            hwnd = win32gui.GetForegroundWindow()
            #hwnd = win32gui.WindowFromPoint(win32gui.GetCursorPos())
            w0, h0, w1, h1 = win32gui.GetWindowRect(hwnd)
            w = w1 - w0
            h = h1 - h0

            if (w == full_w) and (h == full_h):
                return None

            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
            saveDC.SelectObject(saveBitMap)
            saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (0, 0),  win32con.SRCCOPY)
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

            return img

        except:
            return False

    def pil2cv(self, pil_image=None):
        try:
            cv2_image = np.array(pil_image, dtype=np.uint8)
            if (cv2_image.ndim == 2):  # モノクロ
                pass
            elif (cv2_image.shape[2] == 3):  # カラー
                cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)
            elif (cv2_image.shape[2] == 4):  # 透過
                cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGBA2BGRA)
            return cv2_image
        except:
            pass
        return None



if __name__ == '__main__':

    win_shot = win_shot_class()

    out_width  = 640
    out_height = 480

    chktime = time.time()
    while ((time.time() - chktime) <= 3600):

        frm = win_shot.screenshot()
        #frm = win_shot.windowshot()
        if (not frm is None):
            image_img = win_shot.pil2cv(frm)
            if (not image_img is None):

                image_height, image_width = image_img.shape[:2]

                proc_width  = image_width
                proc_height = image_height
                if (proc_width > out_width):
                    proc_width  = out_width
                    proc_height = int(proc_width * image_height / image_width)
                if (proc_width  != image_width ) \
                or (proc_height != image_height):
                    proc_img = cv2.resize(image_img, (proc_width, proc_height))
                else:
                    proc_img = image_img.copy()
                    proc_height, proc_width = proc_img.shape[:2]

                cv2.imshow("", proc_img)
                cv2.waitKey(1)

        time.sleep(1.00)



    cv2.destroyAllWindows()


