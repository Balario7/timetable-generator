@echo off
REM ============================================================
REM Timetable Generator - Run Entire Project (Backend + Frontend)
REM ============================================================

setlocal enabledelayedexpansion

color 0A
title TIMETABLE GENERATOR - STARTUP

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         TIMETABLE GENERATOR - COMPLETE STARTUP             ║
echo ║                                                            ║
echo ║  This script will start:                                  ║
echo ║  1. Backend Server (FastAPI on port 8000)                ║
echo ║  2. Frontend Server (React on port 3000)                 ║
echo ║  PostgreSQL database will be initialized automatically   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check prerequisites
echo [1/5] Checking prerequisites...
echo.

REM Check if PostgreSQL is available
echo [INFO] Checking PostgreSQL connectivity...
python -c "import psycopg2; psycopg2.connect(host='127.0.0.1', port=5432, dbname='postgres', user='postgres', password='hi')" 2>nul
if errorlevel 1 (
    color 04
    cls
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║              ERROR: POSTGRESQL NOT ACCESSIBLE               ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo PostgreSQL is required to run this application.
    echo.
    echo Please ensure PostgreSQL is running with these credentials:
    echo   - User: postgres
    echo   - Password: hi
    echo   - Host: 127.0.0.1
    echo   - Port: 5432
    echo.
    echo To install PostgreSQL:
    echo   https://www.postgresql.org/download/
    echo.
    pause
    exit /b 1
)
color 0A
echo [OK] PostgreSQL is available
echo.

REM Check npm installation
where /q npm
if errorlevel 1 (
    color 04
    cls
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║                 ERROR: NPM NOT INSTALLED                    ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo npm is required but not found in your system.
    echo.
    echo Please install Node.js with npm from:
    echo   https://nodejs.org (Download LTS version)
    echo.
    pause
    exit /b 1
)
color 0A
echo [OK] npm is installed
echo.

REM Check if node_modules exists, if not install
echo [2/5] Checking Node dependencies...
if not exist "node_modules" (
    echo [INFO] Installing npm dependencies...
    call npm install > nul 2>&1
    if errorlevel 1 (
        color 04
        cls
        echo.
        echo ╔════════════════════════════════════════════════════════════╗
        echo ║           ERROR: FAILED TO INSTALL DEPENDENCIES            ║
        echo ╚════════════════════════════════════════════════════════════╝
        echo.
        echo Failed to install npm packages. Please try:
        echo   1. Delete "node_modules" folder
        echo   2. Run "npm install" manually
        echo   3. Run this script again
        echo.
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)
echo.

REM Detect virtual environment
echo [3/5] Detecting Python virtual environment...
if exist "backend\venv\Scripts\activate.bat" (
    set VENV_PATH=backend\venv
    echo [OK] Found venv at backend\venv
) else if exist "backend\venv_new\Scripts\activate.bat" (
    set VENV_PATH=backend\venv_new
    echo [OK] Found venv at backend\venv_new
) else if exist "backend\venv_final\Scripts\activate.bat" (
    set VENV_PATH=backend\venv_final
    echo [OK] Found venv at backend\venv_final
) else (
    color 04
    cls
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║          ERROR: PYTHON VIRTUAL ENVIRONMENT NOT FOUND        ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Virtual environment not found in backend folder.
    echo.
    echo Please run setup.bat first to create the environment:
    echo   .\setup.bat
    echo.
    pause
    exit /b 1
)
echo.

REM All checks passed
color 0A
echo [4/5] All prerequisites met
echo.
echo [5/5] Starting services...
echo.
timeout /t 2 > nul

REM Clear screen and show startup message
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║       TIMETABLE GENERATOR - STARTING ALL SERVICES          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Starting Backend Server...
echo   - Command: FastAPI on localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo.

REM Start Backend in a new window
start "TIMETABLE GENERATOR - Backend" cmd /k "cd backend && call %VENV_PATH%\Scripts\activate.bat && python -m uvicorn app:app --host localhost --port 8000 --reload"

REM Wait for backend to fully start
echo Waiting for backend to fully initialize... (3 seconds)
timeout /t 3 > nul

echo.
echo Starting Frontend Server...
echo   - Command: React on localhost:3000
echo   - URL: http://localhost:3000
echo.

REM Start Frontend in a new window
start "TIMETABLE GENERATOR - Frontend" cmd /k "set NODE_OPTIONS=--openssl-legacy-provider && npm start"

REM Wait for frontend to fully start
echo Waiting for frontend to fully initialize... (5 seconds)
timeout /t 5 > nul

REM Clear and show final message
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         TIMETABLE GENERATOR - ALL SERVICES STARTED         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ✓ MongoDB Server
echo   └─ mongodb://localhost:27017/timetable
echo.
echo ✓ Backend API Server (Port 8000)
echo   └─ http://localhost:8000
echo   └─ API Documentation: http://localhost:8000/docs
echo.
echo ✓ Frontend Web Application (Port 3000)
echo   └─ http://localhost:3000
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo NEXT STEPS:
echo   1. [Recommended] Browser will auto-open at http://localhost:3000
echo   2. If not, manually open: http://localhost:3000 in your browser
echo   3. Add Courses in Tab 1
echo   4. Add Constraints in Tab 2
echo   5. Generate Timetable in Tab 3
echo.
echo USEFUL LINKS:
echo   • Application: http://localhost:3000
echo   • Backend API: http://localhost:8000
echo   • Swagger API Docs: http://localhost:8000/docs
echo   • ReDoc API Docs: http://localhost:8000/redoc
echo.
echo TO TROUBLESHOOT:
echo   • Check Backend window for errors
echo   • Check Frontend window for React errors
echo   • Check browser console (F12) for frontend issues
echo   • Ensure MongoDB is running
echo.
echo TO STOP ALL SERVICES:
echo   • Close the Backend window (Ctrl+C)
echo   • Close the Frontend window (Ctrl+C)
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Open browser automatically
start http://localhost:3000

echo.
echo Opening application in your default browser...
echo.
pause
