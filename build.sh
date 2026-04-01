#!/bin/bash
# Build script for Render deployment

echo "=== Building AI Reel Automation ==="
echo ""

echo "1. Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "2. Checking frontend build..."
if [ -d "Frontend/reel-genius/dist" ] && [ -f "Frontend/reel-genius/dist/index.html" ]; then
    echo "✓ Frontend build found at Frontend/reel-genius/dist"
else
    echo "! Frontend build not found, checking if npm is available..."
    if command -v npm &> /dev/null; then
        echo "  Building frontend..."
        cd Frontend/reel-genius
        npm install
        npm run build
        cd ../..
        echo "✓ Frontend built successfully"
    else
        echo "⚠ npm not available - frontend will not be served"
    fi
fi

echo ""
echo "=== Build complete ==="
