"""
Quick test to verify frontend-backend connection
Run this in PowerShell AFTER both servers are running
"""

import requests
import json
import sys

def test_api():
    print("=" * 60)
    print("TESTING FRONTEND-BACKEND CONNECTION")
    print("=" * 60)
    
    api_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n[TEST 1] Health endpoint...")
    try:
        response = requests.get(f"{api_url}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   → Backend server not running on port 5000!")
        return False
    
    # Test 2: POST request (like frontend does)
    print("\n[TEST 2] Generate endpoint (like frontend does)...")
    try:
        payload = {
            "prompt": "Test motivation reel",
            "language": "en"
        }
        print(f"   Sending: {payload}")
        
        response = requests.post(
            f"{api_url}/api/generate-reel",
            json=payload,
            timeout=5
        )
        
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response headers: {dict(response.headers)}")
        print(f"✅ Connection successful!")
        
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection refused!")
        print(f"   → Backend server not responding")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - Connection is working!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    try:
        success = test_api()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
