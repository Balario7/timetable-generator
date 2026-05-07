@echo off
REM Timetable Generator - Start Frontend Server

echo.
echo ========================================
echo Starting Frontend Server...
echo ========================================
echo.

echo Frontend server starting on http://localhost:3000
echo.
echo Keep this window open to keep the server running!
echo Press Ctrl+C to stop the server
echo.
timeout /t 2

call npm start
