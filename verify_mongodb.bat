@echo off
REM ============================================================
REM Verify MongoDB Connectivity and Check Timetable Details
REM ============================================================

title TIMETABLE GENERATOR - MongoDB Verification

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║      TIMETABLE GENERATOR - MongoDB Verification Script    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Running verification, please wait...
echo.

cd /d "%~dp0"
cd backend

REM Check if venv exists and use it
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist "venv_new\Scripts\activate.bat" (
    call venv_new\Scripts\activate.bat
) else if exist "venv_final\Scripts\activate.bat" (
    call venv_final\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found
    pause
    exit /b 1
)

REM Run verification script
python verify_mongodb_connectivity.py

pause
