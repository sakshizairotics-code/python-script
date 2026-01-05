import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip

# ========================
# SETTINGS
# ========================

W, H = 1080, 1920
MARGIN_X = 90
SHADOW_OFFSET = 3
FPS = 30
DURATION = 5

FONT_FILE = "C:/Windows/Fonts/arial.ttf"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 🔥 IMPORTANT


def hex_to_rgb(hex_color):
    hex_color = str(hex_color).strip().lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def parse_color(value):
    if str(value).startswith("#"):
        return hex_to_rgb(value)
    return (255, 255, 255)


def wrap_text(text, font, max_width):
    words = text.split()
    lines, current = [], ""

    for word in words:
        test = (current + " " + word).strip()
        if font.getbbox(test)[2] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def render_frame(image_path, text_color, font_size, text):
    # 🔥 FIX PATH PROPERLY
    full_image_path = os.path.join(BASE_DIR, image_path)

    if not os.path.exists(full_image_path):
        raise FileNotFoundError(f"Image not found: {full_image_path}")

    bg = Image.open(full_image_path).convert("RGB")
    bg = bg.resize((W, H))

    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(FONT_FILE, int(font_size))
    max_width = W - (2 * MARGIN_X)

    lines = wrap_text(text, font, max_width)

    line_gap = int(font_size * 0.35)
    heights = [font.getbbox(l)[3] for l in lines]
    total_height = sum(heights) + line_gap * (len(lines) - 1)
    y = (H - total_height) // 2

    for line in lines:
        lw = font.getbbox(line)[2]
        x = (W - lw) // 2

        draw.text((x + SHADOW_OFFSET, y + SHADOW_OFFSET),
                  line, font=font, fill=(0, 0, 0))
        draw.text((x, y), line, font=font, fill=text_color)

        y += font.getbbox(line)[3] + line_gap

    return np.array(bg)


def main():
    csv_path = os.path.join(BASE_DIR, "input", "fcbg.csv")
    out_dir = os.path.join(BASE_DIR, "output")

    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(csv_path)

    print("CSV COLUMNS:", df.columns)

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Rendering videos"):
        frame = render_frame(
            row["image"],
            parse_color(row["text_color"]),
            row["font_size"],
            row["text"]
        )

        clip = ImageClip(frame).with_duration(DURATION).with_fps(FPS)
        clip.write_videofile(
            os.path.join(out_dir, f"{row['output_name']}.mp4"),
            codec="libx264",
            audio=False,
            fps=FPS
        )

    print("✅ Videos generated successfully")


if __name__ == "__main__":
    main()
