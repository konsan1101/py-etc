#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/hatt_takumi/items/d65c243294f250724c19

import json
import requests
import wave

import subprocess

def generate_wav(outText, speaker=1, outFile='test_voicevox.wav'):
    host = 'localhost'
    port = 50021
    params = (
        ('text', outText),
        ('speaker', speaker),
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    wf = wave.open(outFile, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response2.content)
    wf.close()

if __name__ == '__main__':
    outText = 'こんにちは！'

    # 女性
    for i in (6,20):
        print(i)
        tmpFile = 'test_voicevox_' + str(i) + '.wav'

        generate_wav(outText=outText, speaker=i, outFile=tmpFile,)

        sox = subprocess.Popen(['sox', tmpFile, '-d', '-q'], )
        sox.wait()
        sox.terminate()
        sox = None

    # 男性
    for i in (11,21):
        print(i)
        tmpFile = 'test_voicevox_' + str(i) + '.wav'

        generate_wav(outText=outText, speaker=i, outFile=tmpFile,)

        sox = subprocess.Popen(['sox', tmpFile, '-d', '-q'], )
        sox.wait()
        sox.terminate()
        sox = None

    # 決定 女性=20,男性=21
    for i in (20,21):
        print(i)
        tmpFile = 'test_voicevox_' + str(i) + '.wav'

        #generate_wav(outText=outText, speaker=i, outFile=tmpFile,)

        sox = subprocess.Popen(['sox', tmpFile, '-d', '-q'], )
        sox.wait()
        sox.terminate()
        sox = None


