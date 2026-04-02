#!/usr/bin/env python
"""
Simple script to generate a reel via API
"""
import requests
import json
import sys

# Default parameters
prompt = 'morning yoga routine for beginners'
language = 'en'
format_type = 'vertical'  # 'vertical' (9:16 - Instagram) or 'horizontal' (16:9)

# Parse command line arguments
if len(sys.argv) > 1:
    prompt = ' '.join(sys.argv[1:])

url = 'http://localhost:5000/api/generate-reel'
data = {
    'prompt': prompt,
    'language': language,
    'format': format_type  # Add format parameter for vertical video
}

print('[*] Sending request to generate reel...')
print(f'[*] Prompt: {data["prompt"]}')
print(f'[*] Format: {format_type.upper()} (9:16 for Instagram Reels)')
print()

try:
    response = requests.post(url, json=data, stream=True)
    
    for line in response.iter_lines():
        if line:
            try:
                event = json.loads(line.decode().split('data: ')[1])
                message = event.get('message', '')
                status = event.get('status', '')
                
                if status == 'active':
                    print(f'  → {message}')
                elif status == 'complete':
                    print(f'  ✓ {message}')
                elif status == 'success':
                    print()
                    print(f'✅ SUCCESS: {message}')
                    print(f'   Video ID: {event.get("video_id")}')
                    print(f'   Duration: {event.get("duration")}')
                    print(f'   Format: VERTICAL (9:16) - Perfect for Instagram Reels!')
                elif status == 'error':
                    print(f'❌ ERROR: {message}')
            except Exception as e:
                pass
                
except Exception as e:
    print(f'❌ Error: {e}')
