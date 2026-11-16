from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
COVER_WIDTH = 1024
COVER_HEIGHT = 1536
BG_COLOR = "#0f172a"  # Dark Slate (matches Quarto slate theme roughly)
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#38bdf8" # Light Blue for subtitle line or accent

# Source Image
SOURCE_IMG = "runner_feature.png"

# Text Content
TITLE = "Statistics for\nMovement Science"
SUBTITLE = "A Hands-On Guide with SPSS | First Edition"
AUTHOR = "Ovande Furtado, Jr., Ph.D."

def create_cover():
    # 1. Create Canvas
    cover = Image.new("RGB", (COVER_WIDTH, COVER_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(cover)
    
    # 2. Load and Place Feature Image
    # Resizing logic: Keep aspect ratio of 1024x1024, maybe scale down slightly to fit nicely in middle?
    # Or just place it. 1024 width fits perfectly.
    if os.path.exists(SOURCE_IMG):
        feature = Image.open(SOURCE_IMG).convert("RGB")
        # Resize if needed? It's 1024x1024.
        # Let's place it vertically centered, slightly shifted up?
        # Canvas 1536. Image 1024. Space left: 512.
        # Top space: 256. Bottom: 256.
        # This leaves room for title at top and author at bottom.
        # Perfect.
        y_pos = (COVER_HEIGHT - feature.height) // 2
        cover.paste(feature, (0, y_pos))
    else:
        print("Feature image not found, skipping.")

    # 3. Typography
    # Try to find a nice font
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    if not os.path.exists(font_path):
        font_path = "/Library/Fonts/Arial.ttf"
    if not os.path.exists(font_path):
        # Fallback to default load_default (bitmap, ugly but works)
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    else:
        font_large = ImageFont.truetype(font_path, 90)
        font_medium = ImageFont.truetype(font_path, 40)
        font_small = ImageFont.truetype(font_path, 50)

    # 4. Draw Title (Top Centered)
    # Multiline title support in PIL depends on version, manual split safer for older PIL
    # "Statistics for"
    # "Movement Science"
    
    # Measure and draw Title
    title_lines = TITLE.split('\n')
    current_y = 100
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        w = bbox[2] - bbox[0]
        x = (COVER_WIDTH - w) // 2
        draw.text((x, current_y), line, font=font_large, fill=TEXT_COLOR)
        current_y += 110 # Line spacing

    # 5. Draw Subtitle (Below Title, above Image)
    # Or below image? "A Hands-On Guide..." might be good below title.
    # Let's put it below the title block.
    current_y += 20
    subtitle_bbox = draw.textbbox((0, 0), SUBTITLE, font=font_medium)
    sub_w = subtitle_bbox[2] - subtitle_bbox[0]
    sub_x = (COVER_WIDTH - sub_w) // 2
    draw.text((sub_x, current_y), SUBTITLE, font=font_medium, fill=ACCENT_COLOR)

    # 6. Draw Author (Bottom Centered)
    author_bbox = draw.textbbox((0, 0), AUTHOR, font=font_small)
    aut_w = author_bbox[2] - author_bbox[0]
    aut_x = (COVER_WIDTH - aut_w) // 2
    
    # Position at bottom with padding
    aut_y = COVER_HEIGHT - 200
    draw.text((aut_x, aut_y), AUTHOR, font=font_small, fill=TEXT_COLOR)

    # Save
    cover.save("cover_new.png")
    print("Cover created successfully.")

if __name__ == "__main__":
    create_cover()
