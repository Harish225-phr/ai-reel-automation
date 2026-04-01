from prompt_parser import PromptParser

# Test structured format
prompt = """Topic: Daily temple benefits
Style: spiritual motivational
Voice: Hindi male
Mood: emotional
Music: calm devotional
Video style: temple + sunrise + meditation"""

result = PromptParser.parse(prompt)

print("PARSED STRUCTURED FORMAT:")
print(f"  Keyword: {result['keyword']}")
print(f"  Language: {result['language']}")
print(f"  Voice: {result['voice_type']}")
print(f"  Mood: {result['mood']}")
print(f"  Music: {result['music_type']}")
print(f"  Theme: {result['video_theme']}")
print(f"  Duration: {result['duration']}s")

voice = PromptParser.get_voice_for_language_and_mood(
    result['language'],
    result['voice_type'],
    result['mood']
)
print(f"  Selected Voice: {voice}")
