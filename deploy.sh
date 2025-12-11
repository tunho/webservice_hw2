#!/bin/bash

# 1. Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# 2. Set environment variables (if not already set)
# export PYTHONPATH=src

# 3. Run the server
echo "Starting server..."
# Use gunicorn for production (if installed) or uvicorn directly
# nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 > app.log 2>&1 &
PYTHONPATH=src uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
