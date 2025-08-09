#!/bin/bash

# Check if .chrome folder exists
if [ ! -d ".chrome" ]; then
    echo "⚡ First run detected. Executing setup..."
    bash utils/first_run.sh
fi