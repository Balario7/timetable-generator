@echo off
REM Timetable Generator - Automated Setup Script for Windows

echo.
echo ========================================
echo Timetable Generator - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if MongoDB is running
echo Checking MongoDB...
mongostat --help >nul 2>&1
if errorlevel 1 (
    echo WARNING: MongoDB tools not found
    echo Please ensure MongoDB is installed and running
    echo You can download it from: https://www.mongodb.com/try/download/community
    pause
)

REM Setup Backend
echo.
echo [1/4] Setting up Backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python packages...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install Python packages
    pause
    exit /b 1
)

REM Add sample data
echo Adding sample data to MongoDB...
python add_sample_data.py
timeout /t 2

REM Go back to root
cd ..

REM Setup Frontend
echo.
echo [2/4] Setting up Frontend...
echo Installing Node packages...
call npm install --quiet

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo [3/4] To start the project, run:
echo   - Run start_backend.bat (Backend on port 8000)
echo   - Run start_frontend.bat (Frontend on port 3000)
echo.
echo [4/4] Open http://localhost:3000 in your browser
echo.
echo For more information, see SETUP_GUIDE.md
echo.
REM pause
