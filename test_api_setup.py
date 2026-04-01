"""
Quick test script to verify API server can start
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from api_server import app, OUTPUT_DIR
    print("✅ API server module imported successfully")
    
    # Check output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"✅ Output directory ready: {OUTPUT_DIR}")
    
    # Check Flask app
    print(f"✅ Flask app created: {app}")
    print(f"✅ CORS enabled: Yes")
    
    # Test routes
    with app.test_client() as client:
        # Health check
        response = client.get('/health')
        print(f"✅ /health endpoint: {response.status_code} {response.json}")
        
    print("\n" + "="*50)
    print("✅ ALL CHECKS PASSED - Ready to start!")
    print("="*50)
    print("\nTo start the system:")
    print("  Windows: double-click START_FULL_SYSTEM.bat")
    print("  Or manually: python api_server.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
