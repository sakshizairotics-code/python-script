# ---------- FIX FOR PILLOW + MOVIEPY ----------
from PIL import Image, ImageDraw, ImageFont

# Pillow 10+ compatibility fix
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# ---------- IMPORTS ----------
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.all import fadein, fadeout
import numpy as np
import os

# ---------- CONFIG ----------
WIDTH, HEIGHT = 1080, 1920
DURATION = 15
FPS = 30

BG_VIDEO = "assets/bg_video.mp4"         # Background video
BG_MUSIC = "assets/sbg_music.wav"        # Background audio
OUTPUT = "output1.mp4"                     # Output file

FONT_FILE = "C:/Windows/Fonts/arial.ttf" # Font path
FONT_SIZE = 64                            # Font size
TEXT_COLOR = "yellow"                     # Text color
SHADOW_COLOR = "black"                    # Shadow color

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

# ---------- FUNCTION TO DRAW TEXT WITH SHADOW ----------
def make_text_frame():
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    # Calculate text size and position
    bbox = draw.multiline_textbbox((0, 0), TEXT, font=font, align="center")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    # Draw shadow
    draw.multiline_text((x+2, y+2), TEXT, font=font, fill=SHADOW_COLOR, align="center")
    # Draw main text
    draw.multiline_text((x, y), TEXT, font=font, fill=TEXT_COLOR, align="center")

    return np.array(img)

# ---------- CREATE TEXT CLIP ----------
text_clip = ImageClip(make_text_frame()).set_duration(DURATION)
text_clip = fadein(text_clip, 1).fadeout(1)  # Fade in/out 1 second

# ---------- LOAD AUDIO ----------
audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION)

# ---------- COMBINE VIDEO + TEXT + AUDIO ----------
final = CompositeVideoClip([bg_clip, text_clip]).set_audio(audio)

# ---------- EXPORT ----------
final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Background video + text + music added successfully with shadow & fade effect")
