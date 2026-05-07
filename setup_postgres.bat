@echo off
REM Setup PostgreSQL Database for Timetable Generator
REM This script assumes PostgreSQL is already installed

echo.
echo ============================================
echo PostgreSQL Database Setup for Timetable
echo ============================================
echo.

REM Check if psql is available
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PostgreSQL is not installed or psql not found in PATH
    echo.
    echo Please install PostgreSQL first from:
    echo https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
)

echo PostgreSQL found: 
psql --version
echo.

REM Get database details from user or use defaults
set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=timetable_db
set DB_USER=postgres

echo Using database configuration:
echo   Host: %DB_HOST%
echo   Port: %DB_PORT%
echo   Database: %DB_NAME%
echo   User: %DB_USER%
echo.

set /p CONFIRM="Is this correct? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Setup cancelled.
    pause
    exit /b 1
)

echo.
echo Attempting to create database...
echo.

REM Create the database
psql -U %DB_USER% -h %DB_HOST% -p %DB_PORT% -tc "SELECT 1 FROM pg_database WHERE datname = '%DB_NAME%'" | findstr /r "^[ ]*1[ ]*$" >nul

if %errorlevel% equ 0 (
    echo Database '%DB_NAME%' already exists.
) else (
    echo Creating database '%DB_NAME%'...
    psql -U %DB_USER% -h %DB_HOST% -p %DB_PORT% -c "CREATE DATABASE %DB_NAME% ENCODING 'UTF8';" 
    
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create database
        echo Please ensure PostgreSQL is running and credentials are correct
        pause
        exit /b 1
    )
    echo Database created successfully!
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Go to backend directory
echo 2. Install Python dependencies: pip install -r requirements.txt
echo 3. Start the backend: python app.py
echo.
pause
