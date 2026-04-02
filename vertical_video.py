#!/usr/bin/env python
"""
Create proper vertical videos (9:16 ratio for Instagram Reels)
"""
from PIL import Image, ImageDraw, ImageFont
import io

def create_vertical_video_frame(text, frame_num, total_frames, width=1080, height=1920):
    """Create a single vertical video frame"""
    
    # Color gradient based on frame
    progress = frame_num / total_frames
    r = int(30 + progress * 70)
    g = int(30 + progress * 90)
    b = int(60 + progress * 160)
    
    # Create image
    img = Image.new('RGB', (width, height), (r, g, b))
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use larger font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Draw main text
    lines = text.split()[:8]  # Max 8 lines
    y_start = 400
    line_spacing = 200
    
    for i, line in enumerate(lines):
        draw.text(
            (100, y_start + (i * line_spacing)),
            line,
            fill=(255, 255, 255),
            font=font
        )
    
    # Draw frame info at bottom
    draw.text(
        (100, 1800),
        f"Frame {frame_num + 1}/{total_frames}",
        fill=(200, 200, 200),
        font=font
    )
    
    return img

def save_frame_as_bytes(img):
    """Convert PIL image to bytes"""
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

if __name__ == '__main__':
    # Create test frame
    frame = create_vertical_video_frame(
        "This is a vertical video\nfor Instagram Reels\n9:16 format",
        0, 24
    )
    frame.save('test_vertical_frame.png')
    print("✓ Vertical video frame created: test_vertical_frame.png")
    print(f"  Size: 1080x1920 (Instagram Reels format)")
