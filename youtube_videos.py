import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip

# =========================
# Quote Video Generator
# =========================

W, H = 1080, 1920
MARGIN_X = 90
SHADOW_OFFSET = 3
FPS = 30

# FIXED SETTINGS (not changeable from CSV)
FONT_FILE = "C:/Windows/Fonts/arial.ttf"
ALIGN = "center"
DURATION = 5


def hex_to_rgb(hex_color):
    hex_color = str(hex_color).strip().lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def parse_color(value):
    v = str(value).strip().lower()
    if v == "white":
        return (255, 255, 255)
    if v == "pink":
        return (0, 0, 0)
    if v.startswith("#"):
        return hex_to_rgb(v)
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


def render_frame(bg_rgb, text_rgb, font_size, text):
    img = Image.new("RGB", (W, H), bg_rgb)
    draw = ImageDraw.Draw(img)

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

        draw.text((x + SHADOW_OFFSET, y + SHADOW_OFFSET), line, font=font, fill=(0, 0, 0))
        draw.text((x, y), line, font=font, fill=text_rgb)

        y += font.getbbox(line)[3] + line_gap

    return np.array(img)


def main(csv_path="input/youtube.csv", out_dir="output"):
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(csv_path)

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Rendering videos"):
        frame = render_frame(
            parse_color(row["bg_color"]),
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

    print("✅ Videos generated successfully!")


if __name__ == "__main__":
    main()
