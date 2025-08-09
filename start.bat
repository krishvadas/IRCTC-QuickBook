@echo off
REM Check if .chrome folder exists
IF NOT EXIST ".venv" (
    echo ✅ First run detected. Executing setup...
    call utils\first_run.bat
)

.venv/scripts/activate
python main.py