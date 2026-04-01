#!/usr/bin/env python3
"""
Pre-flight check before starting the Flask server
Ensures frontend build exists
"""
import subprocess
import sys
from pathlib import Path
import os

def check_frontend():
    """Check if frontend is built, attempt to build if needed"""
    project_root = Path(__file__).parent
    frontend_dist = project_root / "Frontend" / "reel-genius" / "dist"
    index_html = frontend_dist / "index.html"
    
    print("[PREFLIGHT] Checking frontend build...")
    print(f"[PREFLIGHT] Looking for: {index_html}")
    
    if index_html.exists():
        print("[PREFLIGHT] ✓ Frontend build found")
        return True
    
    print("[PREFLIGHT] ! Frontend build not found")
    
    # Try to build if npm is available
    try:
        which_npm = subprocess.run(['which', 'npm'], capture_output=True, timeout=5)
        npm_path = which_npm.stdout.decode().strip()
        
        if npm_path:
            print(f"[PREFLIGHT] Found npm at: {npm_path}")
            print("[PREFLIGHT] Attempting to build frontend...")
            
            frontend_dir = project_root / "Frontend" / "reel-genius"
            
            # Install dependencies
            print("[PREFLIGHT] Installing npm dependencies...")
            result = subprocess.run(
                ['npm', 'install'],
                cwd=str(frontend_dir),
                timeout=300,
                capture_output=True
            )
            
            if result.returncode == 0:
                # Build
                print("[PREFLIGHT] Building frontend...")
                result = subprocess.run(
                    ['npm', 'run', 'build'],
                    cwd=str(frontend_dir),
                    timeout=300,
                    capture_output=True
                )
                
                if result.returncode == 0 and index_html.exists():
                    print("[PREFLIGHT] ✓ Frontend built successfully")
                    return True
                else:
                    print(f"[PREFLIGHT] Build failed: {result.stderr.decode()}")
    except subprocess.TimeoutExpired:
        print("[PREFLIGHT] Build timed out")
    except FileNotFoundError:
        print("[PREFLIGHT] npm not found")
    except Exception as e:
        print(f"[PREFLIGHT] Error: {e}")
    
    print("[PREFLIGHT] ⚠ Frontend will not be available")
    print("[PREFLIGHT] API endpoints will still work")
    return False

if __name__ == "__main__":
    check_frontend()
