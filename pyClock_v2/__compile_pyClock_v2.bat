@echo off
rem cd ".."

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



ECHO;
ECHO -----
ECHO tools
ECHO -----
rem           pip  install --upgrade pip
    python -m pip  install --upgrade pip
    python -m pip  install --upgrade wheel
    python -m pip  install --upgrade setuptools
    python -m pip  install --upgrade pyinstaller

ECHO;
ECHO -------
ECHO etc
ECHO -------
    python -m pip  install --upgrade screeninfo
    python -m pip  install --upgrade pyautogui
    python -m pip  install --upgrade pywin32
    python -m pip  install --upgrade psutil
    python -m pip  install --upgrade rainbow-logging-handler
    python -m pip  install --upgrade pycryptodome

    python -m pip  install --upgrade numpy
    python -m pip  install --upgrade opencv-python
    python -m pip  install --upgrade opencv-contrib-python

    python -m pip  install --upgrade pillow

    python -m pip  install --upgrade pysimplegui
    python -m pip  install --upgrade matplotlib

ECHO;
ECHO -------
ECHO compile
ECHO -------

set pyname=pyClock_v2
set pyname2=pyClock
    echo;
    echo %pyname%.py

    pyinstaller %pyname%.py  -F --log-level ERROR --noconsole --icon="icon_clock.ico"
rem pyinstaller %pyname%.py  -F --log-level ERROR

IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname2%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname2%.exe"
    copy "%pyname%.exe"        "C:\_���L\Player\%pyname2%.exe"
rem del  "%pyname%.exe"

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



