import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, vfx


W, H = 1080, 1920
MARGIN_X = 90
SHADOW_OFFSET = 3
FPS = 30


def hex_to_rgb(hex_color):
    hex_color = str(hex_color).strip().lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def parse_color(value):
    v = str(value).lower()
    if v == "white":
        return (255, 255, 255)
    if v == "black":
        return (0, 0, 0)
    if v.startswith("#"):
        return hex_to_rgb(v)
    return (255, 255, 255)


def wrap_text_to_lines(text, font, max_width):
    words = text.split()
    lines, current = [], ""

    for w in words:
        test = (current + " " + w).strip()
        if font.getbbox(test)[2] <= max_width:
            current = test
        else:
            lines.append(current)
            current = w

    if current:
        lines.append(current)

    return lines


def render_frame(bg_rgb, text_rgb, font_path, font_size, text, align):
    img = Image.new("RGB", (W, H), bg_rgb)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, int(font_size))
    max_width = W - (2 * MARGIN_X)

    lines = wrap_text_to_lines(text, font, max_width)

    line_gap = int(font_size * 0.35)
    heights = [font.getbbox(l)[3] for l in lines]
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    y = (H - total_h) // 2

    for ln in lines:
        lw = font.getbbox(ln)[2]

        if align == "left":
            x = MARGIN_X
        elif align == "right":
            x = W - lw - MARGIN_X
        else:
            x = (W - lw) // 2

        draw.text((x + SHADOW_OFFSET, y + SHADOW_OFFSET), ln, font=font, fill=(0, 0, 0))
        draw.text((x, y), ln, font=font, fill=text_rgb)

        y += font.getbbox(ln)[3] + line_gap

    return np.array(img)


def main(csv_path: str = "input/insta.csv", out_dir: str = "output"):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    for _, row in tqdm(df.iterrows(), total=len(df)):
        frame = render_frame(
            parse_color(row["bg_color"]),
            parse_color(row["text_color"]),
            row["font_file"],
            row["font_size"],
            row["text"],
            row["align"]
        )

        clip = (
    ImageClip(frame)
    .with_duration(duration=10)
    .with_fps(FPS)
    .with_start(0)
    .with_opacity(1)
)


        clip.write_videofile(
            f"{out_dir}/{row['output_name']}.mp4",
            codec="libx264",
            audio=False,
            fps=FPS
        )


if __name__ == "__main__":
    main()












import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip


# =========================
# Quote Video Generator v1
# =========================

W, H = 1080, 1920
MARGIN_X = 90
SHADOW_OFFSET = 3
FPS = 30


def hex_to_rgb(hex_color: str):
    hex_color = str(hex_color).strip().lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def parse_color(value: str):
    v = str(value).strip().lower()
    if v in ("white", "#fff", "fff"):
        return (255, 255, 255)
    if v in ("black", "#000", "000"):
        return (0, 0, 0)
    if v.startswith("#"):
        return hex_to_rgb(v)
    return (255, 255, 255)


def wrap_text_to_lines(text, font, max_width):
    words = text.split()
    lines, current = [], ""

    for w in words:
        test = (current + " " + w).strip()
        if font.getbbox(test)[2] <= max_width:
            current = test
        else:
            lines.append(current)
            current = w

    if current:
        lines.append(current)

    return lines


def render_frame(bg_rgb, text_rgb, font_path, font_size, text, align):
    img = Image.new("RGB", (W, H), bg_rgb)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, int(font_size))
    max_width = W - (2 * MARGIN_X)

    lines = wrap_text_to_lines(text, font, max_width)

    line_gap = int(font_size * 0.35)
    heights = [font.getbbox(l)[3] for l in lines]
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    y = (H - total_h) // 2

    for ln in lines:
        lw = font.getbbox(ln)[2]

        if align == "left":
            x = MARGIN_X
        elif align == "right":
            x = W - lw - MARGIN_X
        else:
            x = (W - lw) // 2

        draw.text((x + SHADOW_OFFSET, y + SHADOW_OFFSET), ln, font=font, fill=(0, 0, 0))
        draw.text((x, y), ln, font=font, fill=text_rgb)

        y += font.getbbox(ln)[3] + line_gap

    return np.array(img)


def main(csv_path: str = "input/youtube.csv", out_dir: str = "output"):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Rendering videos"):
        frame = render_frame(
            parse_color(row["bg_color"]),
            parse_color(row["text_color"]),
            row["font_file"],
            row["font_size"],
            row["text"],
            row["align"]
        )

        clip = ImageClip(frame).with_duration(float(row["duration"])).with_fps(FPS)

        clip.write_videofile(
            os.path.join(out_dir, f"{row['output_name']}.mp4"),
            codec="libx264",
            audio=False,
            fps=FPS
        )

    print("✅ Videos generated successfully!")


if __name__ == "__main__":
    main()
