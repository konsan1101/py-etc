@echo off
rem cd ".."

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



ECHO;
    python -m pip  install --upgrade pyinstaller==5.1
    python -m pip  install --upgrade numpy
    python -m pip  install --upgrade pyautogui
    python -m pip  install --upgrade pysimplegui
    python -m pip  install --upgrade pywin32
    python -m pip  install --upgrade psutil

ECHO;
    python -m pip  install --upgrade pillow
    python -m pip  install --upgrade numpy
    python -m pip  uninstall -y      opencv-python
    python -m pip  install           opencv-python==4.4.0.46
    python -m pip  uninstall -y      opencv-contrib-python
    python -m pip  install           opencv-contrib-python==4.4.0.46

ECHO;
    python -m pip  install --upgrade matplotlib


set pyname=pyClock_v2
set pyname2=pyClock
    echo;
    echo %pyname%.py
rem    pyinstaller %pyname%.py  -F --log-level ERROR --noconsole
    pyinstaller %pyname%.py  -F --log-level ERROR
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname2%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname2%.exe"
    copy "%pyname%.exe"        "C:\_‹¤—L\Player\%pyname2%.exe"
rem del  "%pyname%.exe"

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



