@ECHO OFF

ECHO;
ECHO design選択（入力無しはauto）
SET design=
SET /P design="?"
IF %design%@==@        SET design=auto

ECHO  start "" "pyClock_v2.exe" "analog" "0.7" %design%
      start "" "pyClock_v2.exe" "analog" "0.7" %design%

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

ECHO;
ECHO exit

EXIT
