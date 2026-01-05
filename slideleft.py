from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import VideoClip

W, H = 1080, 1920
FPS = 30
DURATION = 5
FONT_FILE = "C:/Windows/Fonts/arial.ttf"
BG_IMAGE = "assets/bg1.jpg"
TEXT = "Consistency builds success"

def make_frame(t):
    img = Image.open(BG_IMAGE).resize((W, H))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, 64)

    text_w = font.getbbox(TEXT)[2]
    x_start = -text_w
    x_end = (W - text_w) // 2

    progress = min(t / 1.5, 1)   # 1.5 sec slide
    x = int(x_start + (x_end - x_start) * progress)
    y = H // 2

    draw.text((x, y), TEXT, font=font, fill="white")
    return np.array(img)

clip = VideoClip(make_frame, duration=DURATION)
clip.write_videofile("slide_text.mp4", fps=FPS, codec="libx264", audio=False)
