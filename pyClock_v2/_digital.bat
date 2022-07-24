@ECHO OFF

ECHO  start "" "pyClock_v2.exe" "digital" "0.7"
      start "" "pyClock_v2.exe" "digital" "0.7"

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

ECHO;
ECHO exit

EXIT
