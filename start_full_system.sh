#!/bin/bash
# Start AI Reel Generator - Full Stack
# This script starts both Frontend (React) and Backend (Flask) servers

echo ""
echo "===================================="
echo "  AI Reel Generator - Full Stack"
echo "===================================="
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Python virtual environment not found!"
    echo "Please run: python -m venv .venv"
    exit 1
fi

# Activate venv
source .venv/bin/activate

# Install Flask dependencies if needed
echo "[1/3] Checking Flask dependencies..."
pip install -q flask==2.3.3 flask-cors==4.0.0 python-dotenv==1.0.0

# Start API server in background
echo "[2/3] Starting API Server on http://localhost:5000..."
python api_server.py &
API_PID=$!

# Give API server time to start
sleep 2

# Change to Frontend directory and start dev server
echo "[3/3] Starting React Frontend on http://localhost:8080..."
cd Frontend/reel-genius

echo ""
echo "===================================="
echo "  System is ready!"
echo "===================================="
echo ""
echo "Frontend:  http://localhost:8080"
echo "API:       http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start React dev server (blocking in this window)
npm run dev

# Kill API server when done
kill $API_PID 2>/dev/null || true
