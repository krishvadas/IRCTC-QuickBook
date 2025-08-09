@echo off
REM Check if .chrome folder exists
IF NOT EXIST ".chrome" (
    echo ✅ First run detected. Executing setup...
    call utils\first_run.bat
)