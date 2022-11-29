@ECHO OFF

    SET runMode=analog
rem SET runMode=digital
    SET panel=auto

ECHO;
ECHO design‘I‘ði“ü—Í–³‚µ‚Íautoj
SET design=
SET /P design="?"
IF %design%@==@        SET design=auto


ECHO start "" /min "pyClock_v2.exe" "%runMode%" %panel% %design% "0.7"
     start "" /min "pyClock_v2.exe" "%runMode%" %panel% %design% "0.7"

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

ECHO;
ECHO exit

EXIT
