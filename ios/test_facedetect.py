#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/inasawa/items/3e730c338bcefd522fb8

from objc_util import *
from ctypes import c_void_p
import ui
import time

# 全フレームを処理しようとすると動かなくなるのでこの程度で
FRAME_INTERVAL = 6  # 30fps / 6 = 5fps

frame_counter = 0
last_fps_time = time.time()
fps_counter = 0

AVCaptureSession = ObjCClass('AVCaptureSession')
AVCaptureDevice = ObjCClass('AVCaptureDevice')
AVCaptureDeviceInput = ObjCClass('AVCaptureDeviceInput')
AVCaptureVideoDataOutput = ObjCClass('AVCaptureVideoDataOutput')
AVCaptureVideoPreviewLayer = ObjCClass('AVCaptureVideoPreviewLayer')

CIImage    = ObjCClass('CIImage')
CIDetector = ObjCClass('CIDetector')

dispatch_get_current_queue = c.dispatch_get_current_queue
dispatch_get_current_queue.restype = c_void_p

CMSampleBufferGetImageBuffer = c.CMSampleBufferGetImageBuffer
CMSampleBufferGetImageBuffer.argtypes = [c_void_p]
CMSampleBufferGetImageBuffer.restype = c_void_p

CVPixelBufferLockBaseAddress = c.CVPixelBufferLockBaseAddress
CVPixelBufferLockBaseAddress.argtypes = [c_void_p, c_int]
CVPixelBufferLockBaseAddress.restype = None

CVPixelBufferGetWidth = c.CVPixelBufferGetWidth
CVPixelBufferGetWidth.argtypes = [c_void_p]
CVPixelBufferGetWidth.restype = c_int

CVPixelBufferGetHeight = c.CVPixelBufferGetHeight
CVPixelBufferGetHeight.argtypes = [c_void_p]
CVPixelBufferGetHeight.restype = c_int

CVPixelBufferUnlockBaseAddress = c.CVPixelBufferUnlockBaseAddress
CVPixelBufferUnlockBaseAddress.argtypes = [c_void_p, c_int]
CVPixelBufferUnlockBaseAddress.restype = None


def captureOutput_didOutputSampleBuffer_fromConnection_(_self, _cmd, _output, _sample_buffer, _conn):
    global frame_counter, fps_counter, last_fps_time
    global image_width, image_height, faces

    # 性能確認のためビデオデータの実 FPS 表示
    fps_counter += 1
    now = time.time()
    if int(now) > int(last_fps_time):
        label_fps.text = '{:5.2f} fps'.format((fps_counter) / (now - last_fps_time))
        last_fps_time = now
        fps_counter = 0

    # 画像処理は FRAME_INTERVAL 間隔で処理
    if frame_counter == 0:
        # ビデオ画像のフレームデータを取得
        imagebuffer =  CMSampleBufferGetImageBuffer(_sample_buffer)
        # バッファをロック
        CVPixelBufferLockBaseAddress(imagebuffer, 0)

        image_width  = CVPixelBufferGetWidth(imagebuffer)
        image_height = CVPixelBufferGetHeight(imagebuffer)
        ciimage = CIImage.imageWithCVPixelBuffer_(ObjCInstance(imagebuffer))

        # CIDetector により顔検出
        options = {'CIDetectorAccuracy': 'CIDetectorAccuracyHigh'}
        detector = CIDetector.detectorOfType_context_options_('CIDetectorTypeFace', None, options)
        faces = detector.featuresInImage_(ciimage)

        # バッファのロックを解放
        CVPixelBufferUnlockBaseAddress(imagebuffer, 0)

        # 検出した顔の情報を使って表示を更新
        path_view.set_needs_display()

    frame_counter = (frame_counter + 1) % FRAME_INTERVAL

class PathView(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self):
        # 検出した顔の輪郭に合わせて、表示を加工
        if faces is not None and faces.count() != 0:
            # 顔の部分を白く覆う
            ui.set_color((1, 1, 1, 0.9))
            for face in faces:
                face_bounds = face.bounds()
                # カメラの画像は X軸=1920 Y軸=1080
                # View は X軸=375 Y軸=667
                # 画像のX軸Y軸をViewのY軸X軸に対応させ、サイズを調整
                x = face_bounds.origin.y    * self.height / image_width
                y = face_bounds.origin.x    * self.width  / image_height
                w = face_bounds.size.height * self.height / image_width
                h = face_bounds.size.width  * self.width  / image_height
                path = ui.Path.oval(x, y, w * 1.3, h)
                path.fill()

@on_main_thread
def main():
    global path_view, label_fps, faces

    # 画面の回転には対応しておらず
    # iPhoneの画面縦向きでロックした状態で、横長画面で使う想定
    # View のサイズは手持ちの iPhone6 に合わせたもの
    faces = None
    main_view = ui.View(frame=(0, 0, 375, 667))
    path_view = PathView(frame=main_view.frame)
    main_view.name = 'Face Detector'

    sampleBufferDelegate = create_objc_class(
                                'sampleBufferDelegate',
                                methods=[captureOutput_didOutputSampleBuffer_fromConnection_],
                                protocols=['AVCaptureVideoDataOutputSampleBufferDelegate'])
    delegate = sampleBufferDelegate.new()

    session = AVCaptureSession.alloc().init()
    device = AVCaptureDevice.defaultDeviceWithMediaType_('vide')
    _input = AVCaptureDeviceInput.deviceInputWithDevice_error_(device, None)
    if _input:
        session.addInput_(_input)
    else:
        print('Failed to create input')
        return

    output = AVCaptureVideoDataOutput.alloc().init()
    queue = ObjCInstance(dispatch_get_current_queue())
    output.setSampleBufferDelegate_queue_(delegate, queue)
    output.alwaysDiscardsLateVideoFrames = True

    session.addOutput_(output)
    session.sessionPreset = 'AVCaptureSessionPresetHigh' # 1920 x 1080

    prev_layer = AVCaptureVideoPreviewLayer.layerWithSession_(session)
    prev_layer.frame = ObjCInstance(main_view).bounds()
    prev_layer.setVideoGravity_('AVLayerVideoGravityResizeAspectFill')

    ObjCInstance(main_view).layer().addSublayer_(prev_layer)

    # 性能確認のためビデオデータの実 FPS 表示
    label_fps = ui.Label(frame=(0, 0, main_view.width, 30), flex='W', name='fps')
    label_fps.background_color = (0, 0, 0, 0.5)
    label_fps.text_color = 'white'
    label_fps.text = ''
    label_fps.alignment = ui.ALIGN_CENTER

    main_view.add_subview(label_fps)
    main_view.add_subview(path_view)

    session.startRunning()

    main_view.present('sheet')
    main_view.wait_modal()

    session.stopRunning()
    delegate.release()
    session.release()
    output.release()

if __name__ == '__main__':
    main()



