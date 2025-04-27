@echo off
REM Change to specified directory
cd /d %1 || (echo Failed to change directory to %1 && exit /b 1)

REM Clear and write to config.txt
(
    echo %2
    echo %3
    echo %4
) > "..\config.txt" || (echo Failed to write to config.txt && exit /b 1)

REM Run the executable
file.exe
exit