#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://tadaoyamaoka.hatenablog.com/entry/2022/10/15/175722

import soundcard as sc
import numpy as np

import whisper
import threading
import queue
import argparse
import time



LANGAGE       = 'ja'
SAMPLE_RATE   = 16000
CHUNK         = 4096
AUDIO_SEC     = 1
AUDIO_BUFFER  = SAMPLE_RATE * AUDIO_SEC
SPEECH_SEC    = 30
SPEECH_BUFFER = SAMPLE_RATE * SPEECH_SEC



parser = argparse.ArgumentParser()
#parser.add_argument('--model', default='large-v2')
parser.add_argument('--model', default='base')
args = parser.parse_args()

print('Loading model...')
whisper_model = whisper.load_model(args.model)
options = whisper.DecodingOptions(fp16 = False)
print('Done')

q = queue.Queue()



def recognize():
    while True:
        wave = q.get()
        if (len(wave) > 0):
            audio = whisper.pad_or_trim(wave)

            # make log-Mel spectrogram and move to the same device as the model
            mel_model = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

            # detect the spoken language
            _, probs_model = whisper_model.detect_language(mel_model)
            #print(LANGAGE, probs_model[LANGAGE])

            # decode the audio
            result_model = whisper.decode(whisper_model, mel_model, options, language=LANGAGE, )

            # print the recognized text
            if (result_model.text != '') and (result_model.text[:14] != 'ご視聴ありがとうございました'):
                print(f'{max(probs_model, key=probs_model.get)}: {result_model.text}')

        time.sleep(0.5)

th_recognize = threading.Thread(target=recognize, daemon=True)
th_recognize.start()



def audioInput():
    a = 0
    audio_data  = np.empty(AUDIO_BUFFER * 2, dtype=np.float32)
    s = 0
    speech_data = np.empty(SPEECH_BUFFER * 2, dtype=np.float32)

    # start recording
    print(sc.default_microphone().name)
    #print(sc.default_speaker().name)

    with sc.get_microphone(id=str(sc.default_microphone().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE, channels=1) as mic:
    #with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE, channels=1) as mic:

        onece = True
        while True:

            a = 0
            while a < AUDIO_BUFFER:
                wave = mic.record(CHUNK)
                audio_data[a:a+len(wave)] = wave.reshape(-1)
                a += len(wave)

            if ((audio_data[:a] ** 2).max() <= 0.001) or (onece == True):
                onece = False
                print('...')
                a = 0
                if (s != 0):
                    print('recognize... '+ str(s))
                    q.put(speech_data[:s])
                    s = 0

            else:
                print('+++')
                speech_data[s:s+a] = audio_data[:a]
                s += a
                a = 0        
                if (s >= SPEECH_BUFFER):
                    print('recognize... '+ str(s))
                    q.put(speech_data[:s])
                    s = 0

#th_audioInput = threading.Thread(target=audioInput, daemon=True)
#th_audioInput.start()

audioInput()


