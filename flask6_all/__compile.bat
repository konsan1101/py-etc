@echo off
rem cd ".."

rd build /s /q
rd dist /s /q
pause

ECHO;
ECHO pip show              setuptools
     pip show              setuptools
ECHO;
ECHO pip install --upgrade setuptools==44.0.0
ECHO check setuptool version!
ECHO and check jypyter-notebook uninstall!
pause

set pyname=web__RiKi
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
rem copy "%pyname%.exe"        "C:\RiKi_v5_assistant\%pyname%.exe"
rem del  "%pyname%.exe"

echo;
rd build /s /q
rd dist /s /q
pause



