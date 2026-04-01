@echo off
REM Start AI Reel Generator - Complete System
REM This script starts both Frontend (React) and Backend (Flask) servers

echo.
echo ====================================
echo   AI Reel Generator - Full Stack
echo ====================================
echo.

REM Check if venv exists
if not exist .venv (
    echo ERROR: Python virtual environment not found!
    echo Please run: python -m venv .venv
    exit /b 1
)

REM Activate venv
call .venv\Scripts\activate.bat

REM Install Flask dependencies if needed
echo [1/3] Checking Flask dependencies...
pip install -q flask==2.3.3 flask-cors==4.0.0 python-dotenv==1.0.0

REM Start API server in background
echo [2/3] Starting API Server on http://localhost:5000...
start "AI Reel API Server" python api_server.py

REM Give API server time to start
timeout /t 2 /nobreak

REM Change to Frontend directory and start dev server
echo [3/3] Starting React Frontend on http://localhost:8080...
cd Frontend\reel-genius

echo.
echo ====================================
echo   System is ready!
echo ====================================
echo.
echo Frontend:  http://localhost:8080
echo API:       http://localhost:5000
echo.
echo Close this window to stop the servers.
echo (Frontend will stay running in another window)
echo.

REM Start React dev server (blocking in this window)
call npm run dev

pause
