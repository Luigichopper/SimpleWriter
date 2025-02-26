@echo off
echo ============================
echo Novel Writer - Startup Script
echo ============================
echo.

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python 3.7 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Detected Python version: %PYTHON_VERSION%

:: Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment.
        echo Please make sure you have venv package installed.
        echo.
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install or update dependencies
echo Checking dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Warning: Some dependencies could not be installed.
    echo The application may not function correctly.
    echo.
    timeout /t 5
)

:: Ensure required directories exist
if not exist books mkdir books
if not exist extensions mkdir extensions
if not exist templates mkdir templates
if not exist static mkdir static

:: Start the application
echo.
echo Starting Novel Writer...
echo.
echo Access the application in your browser at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server when you're done.
echo.
python main.py

:: Deactivate virtual environment on exit
call venv\Scripts\deactivate.bat

pause
