#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/7shi/items/a5fb03406e0626b4f138

import win32com.client
sapi = win32com.client.Dispatch("SAPI.SpVoice")
cat  = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
cat.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
v = [t for t in cat.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft Sayaka"]
if v:
    fs = win32com.client.Dispatch("SAPI.SpFileStream")
    fs.Open("sayaka.wav", 3)
    sapi.AudioOutputStream = fs
    oldv = sapi.Voice
    sapi.Voice = v[0]
    sapi.Speak("こんにちは、世界")
    sapi.Voice = oldv
    fs.Close()


