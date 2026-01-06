# ---------- FIX FOR PILLOW + MOVIEPY ----------
from PIL import Image, ImageDraw, ImageFont
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# ---------- IMPORTS ----------
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.all import fadein, fadeout
import numpy as np
import os

# ---------- CONFIG ----------
WIDTH, HEIGHT = 1080, 1920
FPS = 30
DURATION = 20

BG_VIDEO = "assets/bg_video.mp4"
BG_MUSIC = "assets/sbg_music.wav"
OUTPUT = "marathi_output.mp4"

# ✅ FONT FROM PROJECT FOLDER
FONT_FILE = "assets/nirmala.ttf"
FONT_SIZE = 64
SHADOW_COLOR = "black"

# ---------- MARATHI TEXT ----------
TEXTS = [
    ("चला निरोप आलाय स्वामीनंचा 😇\n\nजायला लागतं अक्कलकोटला 🙏🏼🙇🏼‍♀️", "black"),
    
]

SLIDE_DURATION = DURATION / len(TEXTS)

# ---------- CHECK FILES ----------
for f in [BG_VIDEO, BG_MUSIC, FONT_FILE]:
    if not os.path.exists(f):
        raise FileNotFoundError(f"❌ Missing file: {f}")

# ---------- BACKGROUND VIDEO ----------
bg_clip = VideoFileClip(BG_VIDEO).subclip(0, DURATION).resize((WIDTH, HEIGHT))

# ---------- TEXT FRAME FUNCTION ----------
def make_text_frame(text, color):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    draw.multiline_text((x+2, y+2), text, font=font, fill=SHADOW_COLOR, align="center")
    draw.multiline_text((x, y), text, font=font, fill=color, align="center")

    return np.array(img)

# ---------- TEXT CLIPS ----------
text_clips = []
for i, (txt, color) in enumerate(TEXTS):
    clip = ImageClip(make_text_frame(txt, color)).set_duration(SLIDE_DURATION)
    clip = fadein(clip, 0.5).fadeout(0.5)
    clip = clip.set_start(i * SLIDE_DURATION).set_position("center")
    text_clips.append(clip)

# ---------- AUDIO ----------
audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION)

# ---------- FINAL ----------
final = CompositeVideoClip([bg_clip, *text_clips]).set_audio(audio)

final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Marathi video created successfully (NO FONT ERROR)")
