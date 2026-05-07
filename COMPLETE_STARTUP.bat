@echo off
REM Complete Startup Script for Timetable Generator

title Timetable Generator - Complete Startup

cls
echo.
echo ============================================
echo Timetable Generator - Startup Script
echo ============================================
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ERROR: Could not find 'backend' directory
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check PostgreSQL connection
echo [1/4] Checking PostgreSQL connection...
psql -U postgres -d timetable_db -c "SELECT version();" >nul 2>&1

if %errorlevel% neq 0 (
    echo ERROR: Cannot connect to PostgreSQL database
    echo.
    echo Solutions:
    echo 1. Is PostgreSQL installed? Download from: https://www.postgresql.org/download/windows/
    echo 2. Is it running? (Check Windows Services for 'postgresql-x64-15')
    echo 3. Database 'timetable_db' created? Run 'setup_postgres.bat'
    echo.
    pause
    exit /b 1
)
echo PostgreSQL OK
echo.

REM Check Python
echo [2/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

REM Check virtual environment
echo [3/4] Setting up Python environment...
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

REM Install requirements
cd backend
pip install -q -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Python packages...
    pip install -r requirements.txt
)
cd ..
echo Python environment ready
echo.

REM Check Node.js
echo [4/4] Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Node.js not found
    echo You need Node.js to run the frontend
    echo Download from: https://nodejs.org/
    echo.
    set SKIP_FRONTEND=1
)

if not "%SKIP_FRONTEND%"=="1" (
    node --version
)
echo.

REM Create startup instructions
echo ============================================
echo Setup Complete! Ready to Start
echo ============================================
echo.
echo To start the application, open 2 PowerShell windows:
echo.
echo WINDOW 1 - Backend (Python/FastAPI):
echo ========================
echo cd "%CD%"
echo .venv\Scripts\Activate.ps1
echo cd backend
echo python app.py
echo.
echo WINDOW 2 - Frontend (React):
echo ========================
echo cd "%CD%"
echo npm start
echo.
echo The application will be available at: http://localhost:3000
echo Backend API at: http://localhost:8000
echo.
echo ============================================
echo.
pause
