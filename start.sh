#!/bin/bash

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "⚡ First run detected. Executing setup..."
    source utils/first_run.sh
fi

# Activate and run
source .venv/bin/activate
python main.py
