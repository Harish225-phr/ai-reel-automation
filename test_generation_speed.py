#!/usr/bin/env python3
import requests
import time
import json

payload = {'prompt': 'quick motivation test', 'language': 'en'}
print('⏱️  TESTING GENERATION WITH STDIN FIX')
print('=' * 60)

start = time.time()
response = requests.post('http://localhost:5000/api/generate-reel', json=payload, stream=True, timeout=300)

for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8', errors='ignore')
        elapsed = time.time() - start
        
        if '[PARSE]' in line_str:
            print(f'[{elapsed:3.0f}s] ✓ Parsing started')
        elif '[SCRIPT]' in line_str:
            print(f'[{elapsed:3.0f}s] ✓ Generating script')
        elif '[STEP 3]' in line_str or '[Downloading' in line_str or 'Fetched' in line_str:
            print(f'[{elapsed:3.0f}s] ✓ Downloading videos')
        elif '[VOICE]' in line_str:
            print(f'[{elapsed:3.0f}s] ✓ Generating voice')
        elif '[MUSIC]' in line_str:
            print(f'[{elapsed:3.0f}s] ✓ Creating music')
        elif '[COMPOSE]' in line_str or 'Composing' in line_str:
            print(f'[{elapsed:3.0f}s] ✓ Compositing video')
        elif 'EXPORTING' in line_str or 'Exporting' in line_str:
            print(f'[{elapsed:3.0f}s] ✓ Encoding MP4...')
        elif '[SUCCESS]' in line_str or 'SUCCESS' in line_str:
            total_time = time.time() - start
            print(f'[{total_time:3.0f}s] ✅ COMPLETE!')
            print(f'\n📊 Total generation time: {total_time:.0f} seconds')
            if total_time < 90:
                print('✅ ULTRA-FAST MODE WORKING!')
            break
