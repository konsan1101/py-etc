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

rem python -m pip  install --upgrade numpy
    python -m pip  install --upgrade numpy==1.24.3
    python -m pip  install --upgrade pycc
rem python -m pip  install --upgrade numba
    python -m pip  install --upgrade numba==0.57.0
    python -m pip  install --upgrade torch
    python -m pip  install --upgrade openai-whisper

    python -m pip  install --upgrade six
    python -m pip  install --upgrade tqdm
    python -m pip  install --upgrade packaging
    python -m pip  install --upgrade tokenizers



ECHO;
ECHO -------
ECHO compile
ECHO -------

set pyname=RiKi_mov2jimakuMov
    echo;
    echo %pyname%.py

rem pyinstaller %pyname%.py  -F --log-level ERROR  --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --collect-data whisper
    pyinstaller %pyname%.py  -F --log-level ERROR  --copy-metadata tokenizers --copy-metadata packaging --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --collect-data whisper

IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
rem del  "%pyname%.exe"

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



