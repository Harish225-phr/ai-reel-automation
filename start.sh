#!/bin/bash
# Startup script for Render deployment - Ephemeral API

set -e

echo "[STARTUP] Creating necessary directories..."
mkdir -p output audio videos images music scripts

echo "[STARTUP] Directories ready"
echo "[STARTUP] Starting LIGHTWEIGHT Ephemeral API (no FFmpeg needed)..."

exec gunicorn api_server_ephemeral:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --access-logfile - --error-logfile -
