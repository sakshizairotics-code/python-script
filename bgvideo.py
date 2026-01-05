# ---------- FIX FOR PILLOW + MOVIEPY ----------
from PIL import Image, ImageDraw, ImageFont

# Pillow 10+ compatibility fix
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# ---------- IMPORTS ----------
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip
import numpy as np
import os

# ---------- CONFIG ----------
WIDTH, HEIGHT = 1080, 1920
DURATION = 15

BG_VIDEO = "assets/bg_video.mp4"
BG_MUSIC = "assets/sbg_music.wav"  # <-- add your music here
OUTPUT = "output.mp4"

FONT_FILE = "C:/Windows/Fonts/arial.ttf"
FONT_SIZE = 64

# ---------- TEXT ----------
TEXT = """finally the farewell

call has come from swami

its time to go to akkalkot"""

# ---------- CHECK FILES ----------
if not os.path.exists(BG_VIDEO):
    raise FileNotFoundError(f"Background video not found: {BG_VIDEO}")

if not os.path.exists(BG_MUSIC):
    raise FileNotFoundError(f"Background music not found: {BG_MUSIC}")

# ---------- LOAD BACKGROUND VIDEO ----------
bg_clip = VideoFileClip(BG_VIDEO).subclip(0, DURATION)
bg_clip = bg_clip.resize((WIDTH, HEIGHT))

# ---------- CREATE TEXT FRAME ----------
def make_text_frame():
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    bbox = draw.multiline_textbbox((0, 0), TEXT, font=font, align="center")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    draw.multiline_text((x, y), TEXT, fill="black", font=font, align="center")
    return np.array(img)

text_clip = ImageClip(make_text_frame()).set_duration(DURATION)

# ---------- LOAD AUDIO ----------
audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION)

# ---------- FINAL VIDEO ----------
final = CompositeVideoClip([bg_clip, text_clip]).set_audio(audio)

final.write_videofile(
    OUTPUT,
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Background video + text + music added successfully")
