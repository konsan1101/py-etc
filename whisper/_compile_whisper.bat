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

    python -m pip  install --upgrade huggingface_hub
    python -m pip  install --upgrade pyannote.audio

rem python -m pip  install --upgrade torch
rem python -m pip  install --upgrade whisper

ECHO;
ECHO -------
ECHO compile
ECHO -------

set pyname=speech_api_whisper
    echo;
    echo %pyname%.py

    pyinstaller %pyname%.py  -F --log-level ERROR
rem pyinstaller %pyname%.py  -F --log-level ERROR --hidden-import=pytorch --collect-data torch --copy-metadata torch --copy-metadata tqdm --copy-metadata regex --copy-metadata sacremoses --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --copy-metadata importlib_metadata --hidden-import="sklearn.utils._cython_blas" --hidden-import="sklearn.neighbors.typedefs" --hidden-import="sklearn.neighbors.quad_tree" --hidden-import="sklearn.tree" --hidden-import="sklearn.tree._utils"
rem pyinstaller %pyname%.py  -F --log-level ERROR --hidden-import=torch --collect-data torch --copy-metadata torch --hidden-import=tqdm --copy-metadata tqdm
rem pyinstaller %pyname%.py  -F --log-level ERROR --hidden-import=whisper
rem pyinstaller %pyname%.py  -F --log-level ERROR --noconsole

IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
rem del  "%pyname%.exe"

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



