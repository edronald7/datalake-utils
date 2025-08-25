#!/bin/bash
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment is already activated."
fi
python run.py
