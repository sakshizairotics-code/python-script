from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import VideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os

# ---------- CONFIG ----------
W, H = 1080, 1920
FPS = 30
DURATION = 5

FONT_FILE = "C:/Windows/Fonts/arial.ttf"

BG_IMAGE = "assets/bg3.jpg"

TEXT = "Focus on your goals"
TEXT_COLOR = "black"
BASE_FONT_SIZE = 60

# 🔊 PUT YOUR REAL AUDIO FULL PATH HERE
AUDIO_FILE = r"C:\Users\Sakshi\Desktop\sonali\bg_music.mp3"
AUDIO_VOLUME = 0.5
# ---------------------------

# ❌ Stop if audio not found
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

def make_frame(t):
    img = Image.open(BG_IMAGE).resize((W, H))
    draw = ImageDraw.Draw(img)

    # Slide from left (0–2 sec)
    slide_progress = min(t / 2, 1)
    x_start = -800
    x_center = W // 2

    # Zoom in (2–4 sec)
    zoom_progress = max((t - 2) / 2, 0)
    zoom = 1 + 0.3 * min(zoom_progress, 1)

    font_size = int(BASE_FONT_SIZE * zoom)
    font = ImageFont.truetype(FONT_FILE, font_size)

    bbox = font.getbbox(TEXT)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = int(x_start + slide_progress * (x_center - text_w // 2 - x_start))
    y = (H - text_h) // 2

    draw.text((x, y), TEXT, font=font, fill=TEXT_COLOR)
    return np.array(img)

# 🎬 Create video
video = VideoClip(make_frame, duration=DURATION).with_fps(FPS)

# 🔊 Load & trim audio
audio = (
    AudioFileClip(AUDIO_FILE)
    .subclipped(0, DURATION)
    .with_volume_scaled(AUDIO_VOLUME)
)

# 🎥 Combine video + audio
final = video.with_audio(audio)

final.write_videofile(
    "FINAL_VIDEO_WITH_MUSIC.mp4",
    codec="libx264",
    audio_codec="aac",
    fps=FPS
)

print("✅ FINAL_VIDEO_WITH_MUSIC.mp4 created successfully")
