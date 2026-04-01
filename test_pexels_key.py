"""Test Pexels API key"""
import requests

PEXELS_API_KEY = "WpFsET9nVh30a0g2qOErgaePd7GuA7D8HKfOUFcaeLTJr6C6xHGT7nFv"
PEXELS_BASE = 'https://api.pexels.com/videos/search'

try:
    headers = {'Authorization': PEXELS_API_KEY}
    params = {'query': 'motivation', 'per_page': 3, 'page': 1}
    
    response = requests.get(PEXELS_BASE, headers=headers, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        videos = data.get('videos', [])
        print(f"✓ API key is VALID! Found {len(videos)} videos")
        for video in videos[:2]:
            print(f"  - Video ID {video['id']}: {video['duration']}s")
    elif response.status_code == 401:
        print("✗ API key INVALID (401 Unauthorized)")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text[:200])
        
except Exception as e:
    print(f"✗ Exception: {e}")
