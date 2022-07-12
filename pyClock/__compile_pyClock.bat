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
    python -m pip  install --upgrade pyqt5
    python -m pip  install --upgrade pyqtgraph
    python -m pip  install --upgrade pyautogui



set pyname=pyClock
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR --noconsole
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    copy "%pyname%.exe"        "C:\_‹¤—L\Player\%pyname%.exe"
rem del  "%pyname%.exe"

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



