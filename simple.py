from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import VideoClip, ImageClip, CompositeVideoClip
import textwrap

# ---------- CONFIG ----------
W, H = 1080, 1920
DURATION = 8
FPS = 30
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"
FONT_SIZE = 72
TEXT_COLOR = "white"
OUTPUT = "text_video.mp4"

TEXT = (
    "Some moments\n\n"
    "are not captured\n"
    "by camera,\n\n"
    "but by heart."
)

# ---------- TEXT IMAGE ----------
def create_text_image(text):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    lines = []
    for line in text.split("\n"):
        wrapped = textwrap.wrap(line, width=22)
        lines.extend(wrapped if wrapped else [""])

    total_height = sum(font.getbbox(line)[3] for line in lines)
    y = (H - total_height) // 2

    for line in lines:
        w, h = font.getbbox(line)[2:]
        x = (W - w) // 2
        draw.text((x, y), line, font=font, fill=TEXT_COLOR)
        y += h + 15

    return np.array(img)

# ---------- ANIMATED BACKGROUND ----------
def animated_bg(t):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        r = int(60 + 60 * np.sin(t + y / 300))
        g = int(40 + 80 * np.cos(t + y / 400))
        b = int(120 + 80 * np.sin(t + y / 500))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    return np.array(img)

# ---------- CLIPS ----------
bg_clip = VideoClip(make_frame=animated_bg, duration=DURATION).set_fps(FPS)

text_img = create_text_image(TEXT)

text_clip = (
    ImageClip(text_img)
    .set_duration(DURATION)
    .set_position("center")
    .fadein(1)
    .fadeout(1)
)

final = CompositeVideoClip([bg_clip, text_clip], size=(W, H))

final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio=False
)

print("✅ Video created successfully")
