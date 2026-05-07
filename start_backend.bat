@echo off
REM Timetable Generator - Start Backend Server

echo.
echo ========================================
echo Starting Backend Server...
echo ========================================
echo.

cd backend

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the backend server
echo Backend server starting on http://127.0.0.1:8000
echo.
echo Keep this window open to keep the server running!
echo Press Ctrl+C to stop the server
echo.
timeout /t 2

python app.py

pause
