# ================================
# Animated Gradient Video Generator
# ================================

from PIL import Image

# ---- Pillow 10+ FIX ----
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import (
    VideoClip,
    ImageClip,
    CompositeVideoClip,
    AudioFileClip
)
from PIL import ImageDraw, ImageFont
import numpy as np
import textwrap
import os

# ---------------- CONFIG ----------------
W, H = 1080, 1920
DURATION = 10
FPS = 30
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"
FONT_SIZE = 70
TEXT_COLOR = "white"
OUTPUT = "animated_video.mp4"
BG_MUSIC = None   # optional

TEXT = (
    "Some days\n\n"
    "are meant to be felt,\n"
    "not explained."
)

# ---------------- TEXT IMAGE ----------------
def create_text_image(text):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    lines = []
    for line in text.split("\n"):
        wrapped = textwrap.wrap(line, width=22)
        lines.extend(wrapped if wrapped else [""])

    total_height = sum(font.getbbox(line)[3] for line in lines)
    y = (H - total_height) // 2   # ✅ CENTER VERTICALLY

    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2]
        text_height = bbox[3]

        x = (W - text_width) // 2  # ✅ CENTER HORIZONTALLY
        draw.text((x, y), line, font=font, fill=TEXT_COLOR)
        y += text_height + 12

    return np.array(img)

# ---------------- ANIMATED GRADIENT ----------------
def gradient_bg(t):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        r = int(40 + 40 * np.sin(t + y / 300))
        g = int(20 + 60 * np.cos(t + y / 400))
        b = int(80 + 80 * np.sin(t + y / 500))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    return np.array(img)

# ---------------- BACKGROUND CLIP ----------------
bg_clip = (
    VideoClip(make_frame=gradient_bg, duration=DURATION)
    .set_fps(FPS)
    .resize(lambda t: 1 + 0.015 * t)   # smooth zoom
)

# ---------------- TEXT CLIP ----------------
text_img = create_text_image(TEXT)   # ✅ FIXED

text_clip = (
    ImageClip(text_img)
    .set_duration(DURATION)
    .set_position("center")          # ✅ EXACT CENTER
    .fadein(1)
    .fadeout(1)
)

# ---------------- COMPOSITE ----------------
final = CompositeVideoClip(
    [bg_clip, text_clip],
    size=(W, H)
)

# ---------------- MUSIC (OPTIONAL) ----------------
if BG_MUSIC and os.path.exists(BG_MUSIC):
    audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION).volumex(0.5)
    final = final.set_audio(audio)

# ---------------- EXPORT ----------------
final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Video created successfully!")
