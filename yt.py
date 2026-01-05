import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip

# =========================
# Quote Video Generator
# =========================

W, H = 1080, 1920
MARGIN_X = 90
SHADOW_OFFSET = 3
FPS = 30
DURATION = 5  # seconds

FONT_FILE = "C:/Windows/Fonts/arial.ttf"

# BACKGROUND COLOR TRANSITION
START_BG = (2, 6, 23)     # dark blue
END_BG   = (88, 28, 135)  # purple


def parse_color(value):
    v = str(value).strip().lower()
    if v == "white":
        return (255, 255, 255)
    if v.startswith("#"):
        v = v.lstrip("#")
        return tuple(int(v[i:i+2], 16) for i in (0, 2, 4))
    return (255, 255, 255)


def interpolate_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


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


def render_frames(text, text_color, font_size):
    frames = []
    total_frames = FPS * DURATION

    font = ImageFont.truetype(FONT_FILE, int(font_size))
    max_width = W - (2 * MARGIN_X)

    lines = wrap_text(text, font, max_width)
    line_gap = int(font_size * 0.35)

    heights = [font.getbbox(l)[3] for l in lines]
    total_height = sum(heights) + line_gap * (len(lines) - 1)
    start_y = (H - total_height) // 2

    for i in range(total_frames):
        t = i / total_frames
        bg_color = interpolate_color(START_BG, END_BG, t)

        img = Image.new("RGB", (W, H), bg_color)
        draw = ImageDraw.Draw(img)

        y = start_y
        for line in lines:
            lw = font.getbbox(line)[2]
            x = (W - lw) // 2

            draw.text((x + SHADOW_OFFSET, y + SHADOW_OFFSET), line, font=font, fill=(0, 0, 0))
            draw.text((x, y), line, font=font, fill=text_color)

            y += font.getbbox(line)[3] + line_gap

        frames.append(np.array(img))

    return frames


def main(csv_path="input/yt.csv", out_dir="output"):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Rendering videos"):
        frames = render_frames(
            row["text"],
            parse_color(row["text_color"]),
            row["font_size"]
        )

        clip = ImageSequenceClip(frames, fps=FPS)

        clip.write_videofile(
            os.path.join(out_dir, f"{row['output_name']}.mp4"),
            codec="libx264",
            audio=False
        )

    print("✅ Videos generated successfully!")


if __name__ == "__main__":
    main()
