from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import VideoClip

# ---------- CONFIG ----------
W, H = 1080, 1920
FPS = 30
DURATION = 5
FONT_FILE = "C:/Windows/Fonts/arial.ttf"
BG_IMAGE = "assets/bg3.jpg"
TEXT = "Focus on your goals"
TEXT_COLOR = "black"
BASE_FONT_SIZE = 60
# ---------------------------

def make_frame(t):
    img = Image.open(BG_IMAGE).resize((W, H))
    draw = ImageDraw.Draw(img)

    # -------- SLIDE FROM LEFT (0s → 2s) --------
    slide_progress = min(t / 2, 1)   # 0 → 1
    x_start = -800                   # outside screen
    x_center = W // 2

    # -------- ZOOM IN (after slide) --------
    zoom_progress = max((t - 2) / 2, 0)
    zoom = 1 + 0.3 * min(zoom_progress, 1)

    font_size = int(BASE_FONT_SIZE * zoom)
    font = ImageFont.truetype(FONT_FILE, font_size)

    text_w = font.getbbox(TEXT)[2]
    text_h = font.getbbox(TEXT)[3]

    x = int(x_start + slide_progress * (x_center - text_w // 2 - x_start))
    y = (H - text_h) // 2

    draw.text((x, y), TEXT, font=font, fill=TEXT_COLOR)
    return np.array(img)

clip = VideoClip(make_frame, duration=DURATION)
clip.write_videofile(
    "slide_left_zoom_text.mp4",
    fps=FPS,
    codec="libx264",
    audio=False
)
