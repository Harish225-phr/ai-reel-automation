"""Test speed improvements with optimizations"""
import requests
import time
import json

# TEST 1: First generation (will download videos)
payload = {'prompt': 'morning yoga stretching', 'language': 'en'}
print('⏱️  TEST 1: First generation (downloads videos)')
print('━' * 50)
start = time.time()

response = requests.post('http://localhost:5000/api/generate-reel', json=payload, stream=True, timeout=300)

success = False
for line in response.iter_lines():
    if line and b'SUCCESS' in line:
        success = True
        elapsed = time.time() - start
        print(f'✓ TEST 1 Generated in {elapsed:.0f} seconds')
        break
    if line and b'Downloaded' in line:
        print('[↓ Downloading videos...]')

print()
print('⏱️  TEST 2: Same keyword (should use cache - MUCH FASTER!)')
print('━' * 50)

start2 = time.time()
response2 = requests.post('http://localhost:5000/api/generate-reel', json=payload, stream=True, timeout=300)

for line in response2.iter_lines():
    if line and b'CACHE' in line:
        print('[⚡ CACHE HIT - skipping download!]')
    if line and b'SUCCESS' in line:
        elapsed2 = time.time() - start2
        print(f'✓ TEST 2 Generated in {elapsed2:.0f} seconds')
        if success:
            improvement = ((elapsed - elapsed2) / elapsed) * 100
            print(f'⚡ SPEEDUP: {improvement:.0f}% faster!')
        break
