#!/bin/bash

echo "============================"
echo "Novel Writer - Startup Script"
echo "============================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in your PATH."
    echo "Please install Python 3.7 or higher from https://www.python.org/downloads/"
    echo "or use your system's package manager."
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Detected Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        echo "Please make sure you have the venv package installed."
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install or update dependencies
echo "Checking dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Warning: Some dependencies could not be installed."
    echo "The application may not function correctly."
    echo
    sleep 5
fi

# Ensure required directories exist
mkdir -p books extensions templates static

# Start the application
echo
echo "Starting Novel Writer..."
echo
echo "Access the application in your browser at: http://127.0.0.1:5000"
echo
echo "Press Ctrl+C to stop the server when you're done."
echo
python main.py

# Deactivate virtual environment on exit
deactivate

read -p "Press Enter to exit..."
