@echo off
REM Check if .venv folder exists
echo [*] Checking requirements...
IF NOT EXIST ".venv" (
    echo ⚡ First run detected. Executing setup...
    call utils\first_run.bat
    goto :run
)

REM Activate and run
:run
echo [>] Activating virtual environment...
call .venv\Scripts\activate.bat
echo [✓] Starting app...
python main.py