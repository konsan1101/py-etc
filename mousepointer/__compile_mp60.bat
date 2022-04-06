@echo off
rem cd ".."

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



ECHO;
ECHO ---------------------------
ECHO pyinstaller compile setting
ECHO ---------------------------
rem rem  python -m pip  install --upgrade setuptools
rem rem  python -m pip  uninstall -y      setuptools
rem rem  python -m pip  install           setuptools==56.0.0
rem rem  python -m pip  install --upgrade pyinstaller
rem rem  python -m pip  uninstall -y      pyinstaller
rem rem  python -m pip  install           pyinstaller==4.3
rem rem  python -m pip  install --upgrade numpy
rem      python -m pip  uninstall -y      numpy
rem      python -m pip  install           numpy==1.20.2
rem rem  python -m pip  install --upgrade matplotlib
rem      python -m pip  uninstall -y      matplotlib
rem      python -m pip  install           matplotlib==3.2.2
rem rem  python -m pip  install --upgrade pandas
rem      python -m pip  uninstall -y      pandas
rem      python -m pip  install           pandas==1.3.5
rem rem  python -m pip  install --upgrade opencv-python
         python -m pip  uninstall -y      opencv-python
         python -m pip  install           opencv-python==4.4.0.46
rem rem  python -m pip  install --upgrade opencv-contrib-python
         python -m pip  uninstall -y      opencv-contrib-python
         python -m pip  install           opencv-contrib-python==4.4.0.46
ECHO;



set pyname=MousePointer60
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    del  "%pyname%.exe"

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



