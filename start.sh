#!/bin/bash

# Check if .chrome folder exists
if [ ! -d ".venv" ]; then
    echo "⚡ First run detected. Executing setup..."
    bash utils/first_run.sh
fi

source venv/bin/activate
python main.py