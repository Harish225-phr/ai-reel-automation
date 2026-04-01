#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from prompt_parser import PromptParser
from script_generator_smart import SmartScriptGenerator
import time

prompt = 'fast coding motivation'
print(f'Testing prompt: {prompt}')
print('=' * 50)

# Test parser
print('[1/2] Testing parser...')
start = time.time()
parsed = PromptParser.parse(prompt)
parser_time = time.time() - start
print(f'Parser time: {parser_time:.3f}s')

# Test script generator  
print('[2/2] Testing script generation...')
start = time.time()
try:
    script = SmartScriptGenerator.generate_script(
        keyword=parsed.get('keyword', 'motivation'),
        mood=parsed.get('mood', 'motivational'),
        duration=parsed.get('duration', 30)
    )
    gen_time = time.time() - start
    print(f'Script gen time: {gen_time:.3f}s')
    print(f'Script length: {len(script)} chars')
    print('=' * 50)
    print(f'TOTAL TIME: {parser_time + gen_time:.3f}s')
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
