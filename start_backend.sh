#!/bin/bash

echo "Starting Stock Tracker Backend..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start the FastAPI server
echo "Starting FastAPI server on http://localhost:8000"
python main.py