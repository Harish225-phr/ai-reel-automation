#!/bin/bash
# Startup script for Render deployment

set -e

echo "[STARTUP] Creating necessary directories..."
mkdir -p output
mkdir -p audio
mkdir -p videos
mkdir -p images
mkdir -p music
mkdir -p scripts

echo "[STARTUP] Directories ready"
echo "[STARTUP] Starting API server with gunicorn..."

exec gunicorn api_server:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --access-logfile - --error-logfile -
