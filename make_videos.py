import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip


# =========================
# Quote Video Generator v1
# =========================
# Creates vertical 9:16 videos (1080x1920), 30 seconds each (or as per CSV),
# showing 1 quote (1–4 lines; auto-wrapped) on a solid background.
#
# Input:  input/quotes.csv
# Output: output/<output_name>.mp4
#
# Notes:
# - Requires FFmpeg installed on your system (MoviePy uses it).
# - Requires a .ttf font file path in CSV (recommended: put fonts inside input/fonts).
#
# Edit these if needed:
W, H = 1080, 1920          # 9:16 vertical
MARGIN_X = 90              # left/right padding for text
SHADOW_OFFSET = 3          # shadow to improve readability
FPS = 30                   # output video fps


def hex_to_rgb(hex_color: str):
    """Convert #RRGGBB to (R,G,B)."""
    hex_color = str(hex_color).strip().lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def parse_color(value: str):
    """Accept 'white', 'black', '#RRGGBB'."""
    v = str(value).strip().lower()
    if v in ("white", "#fff", "fff"):
        return (255, 255, 255)
    if v in ("black", "#000", "000"):
        return (0, 0, 0)
    if v.startswith("#") and len(v) in (4, 7):
        # allow #fff shorthand
        if len(v) == 4:
            v = "#" + "".join([c * 2 for c in v[1:]])
        return hex_to_rgb(v)
    # fallback (white)
    return (255, 255, 255)


def wrap_text_to_lines(text: str, font: ImageFont.FreeTypeFont, max_width_px: int):
    """
    Wrap text so each line fits within max_width_px.
    This keeps the quote readable on mobile screens.
    """
    words = str(text).split()
    lines = []
    current = ""

    for w in words:
        test = (current + " " + w).strip()
        # getbbox returns (x0, y0, x1, y1)
        if font.getbbox(test)[2] <= max_width_px:
            current = test
        else:
            if current:
                lines.append(current)
            current = w

    if current:
        lines.append(current)

    return lines


def render_frame(bg_rgb, text_rgb, font_path, font_size, text, align="center"):
    """
    Render a single 1080x1920 RGB image frame with wrapped quote text.
    """
    img = Image.new("RGB", (W, H), bg_rgb)
    draw = ImageDraw.Draw(img)

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font not found: {font_path}")

    font_size = int(float(font_size))
    font = ImageFont.truetype(font_path, font_size)

    max_text_width = W - (2 * MARGIN_X)

    # Wrap lines to fit width
    lines = wrap_text_to_lines(text, font, max_text_width)

    # Safety: if too many lines, auto-reduce font size a bit
    while len(lines) > 6 and font_size > 36:
        font_size -= 4
        font = ImageFont.truetype(font_path, font_size)
        lines = wrap_text_to_lines(text, font, max_text_width)

    # Measure total height to vertically center the block
    line_gap = int(font_size * 0.35)
    widths, heights = [], []
    for ln in lines:
        bbox = font.getbbox(ln)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])

    total_h = sum(heights) + line_gap * (len(lines) - 1)
    y = (H - total_h) // 2  # start y

    shadow_rgb = (0, 0, 0)

    for i, ln in enumerate(lines):
        lw, lh = widths[i], heights[i]

        a = str(align).strip().lower()
        if a == "left":
            x = MARGIN_X
        elif a == "right":
            x = W - MARGIN_X - lw
        else:
            x = (W - lw) // 2

        # shadow
        draw.text((x + SHADOW_OFFSET, y + SHADOW_OFFSET), ln, font=font, fill=shadow_rgb)
        # main text
        draw.text((x, y), ln, font=font, fill=text_rgb)

        y += lh + line_gap

    return np.array(img)


def main(csv_path: str = "input/quotes.csv", out_dir: str = "output"):
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(csv_path)

    required_cols = [
        "output_name", "text", "duration",
        "bg_color", "text_color", "font_file", "font_size", "align"
    ]
    for c in required_cols:
        if c not in df.columns:
            raise ValueError(f"Missing column in CSV: {c}")

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Rendering videos"):
        output_name = str(row["output_name"]).strip()
        text = str(row["text"]).strip()
        duration = float(row["duration"])

        bg_rgb = parse_color(row["bg_color"])
        text_rgb = parse_color(row["text_color"])
        font_path = str(row["font_file"]).strip()
        font_size = row["font_size"]
        align = str(row["align"]).strip()

        frame = render_frame(bg_rgb, text_rgb, font_path, font_size, text, align)

        out_path = os.path.join(out_dir, f"{output_name}.mp4")

        clip = ImageClip(frame).with_duration(duration).with_fps(FPS)

        # Write MP4 (H.264). MoviePy uses FFmpeg under the hood.
        clip.write_videofile(
            out_path,
            codec="libx264",
            fps=FPS,
            audio=False,
            preset="medium",
            threads=4
        )

    print(f"\n✅ Done. Videos saved in: {out_dir}")


if __name__ == "__main__":
    main()
