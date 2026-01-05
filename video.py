# ---------- FIX FOR PILLOW + MOVIEPY ----------
from PIL import Image

# Pillow 10+ compatibility fix
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# ---------- IMPORTS ----------
from moviepy.editor import VideoFileClip
import os

# ---------- CONFIG ----------
WIDTH, HEIGHT = 1080, 1920
DURATION = 15

BG_VIDEO = "assets/bg_video.mp4"
OUTPUT = "output.mp4"

# ---------- CHECK FILE ----------
if not os.path.exists(BG_VIDEO):
    raise FileNotFoundError(f"Background video not found: {BG_VIDEO}")

# ---------- LOAD BACKGROUND VIDEO ----------
clip = VideoFileClip(BG_VIDEO).subclip(0, DURATION)

# ✅ SAFE RESIZE (NO ERROR)
clip = clip.resize((WIDTH, HEIGHT))

# ---------- EXPORT ----------
clip.write_videofile(
    OUTPUT,
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Background video set successfully (NO ERRORS)")
