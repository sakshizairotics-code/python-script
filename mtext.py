# ---------- PIL + MOVIEPY FIX ----------
from PIL import Image, ImageDraw, ImageFont
Image.ANTIALIAS = Image.Resampling.LANCZOS

# ---------- IMPORTS ----------
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.all import fadein, fadeout
import numpy as np
import os

# ---------- CONFIG ----------
WIDTH, HEIGHT = 1080, 1920
FPS = 30
DURATION = 15

BG_VIDEO = "assets/bg_video.mp4"
BG_MUSIC = "assets/sbg_music.wav"
OUTPUT = "marathi_final.mp4"

FONT_FILE = "assets/nirmala.ttf"   # ✅ Marathi font
FONT_SIZE = 64

# ---------- MARATHI TEXT ----------
TEXT = """चला निरोप आलाय स्वामीनंचा 😇

जायला लागतं अक्कलकोटला 🙏🏼🙇🏼‍♀️"""

# ---------- FILE CHECK ----------
for f in [BG_VIDEO, BG_MUSIC, FONT_FILE]:
    if not os.path.exists(f):
        raise FileNotFoundError(f"❌ Missing file: {f}")

# ---------- BACKGROUND VIDEO ----------
bg = VideoFileClip(BG_VIDEO).subclip(0, DURATION)
bg = bg.resize((WIDTH, HEIGHT))

# ---------- TEXT IMAGE FUNCTION ----------
def make_text_frame():
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    bbox = draw.multiline_textbbox((0, 0), TEXT, font=font, align="center")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    # Shadow
    draw.multiline_text((x+2, y+2), TEXT, font=font, fill="black", align="center")
    # Main text
    draw.multiline_text((x, y), TEXT, font=font, fill="yellow", align="center")

    return np.array(img)

# ---------- TEXT CLIP ----------
text_clip = ImageClip(make_text_frame()) \
    .set_duration(DURATION) \
    .set_position("center")

text_clip = fadein(text_clip, 1).fadeout(1)

# ---------- AUDIO ----------
audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION)

# ---------- FINAL VIDEO ----------
final = CompositeVideoClip([bg, text_clip]).set_audio(audio)

final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Marathi video created successfully (NO ImageMagick needed)")
