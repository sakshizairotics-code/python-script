import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout

# ---------------- CONFIG ----------------
W, H = 1080, 1920
FPS = 30
SLIDE_DURATION = 4

FONT_FILE = "C:/Windows/Fonts/seguiemj.ttf"
TEXT_FILE = "texts.txt"
OUTPUT = "auto_reel1.mp4"

# Backgrounds
BG_IMAGES = [
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg8.jpg"

]

# ---------------- TEXT ----------------
texts = [
    "This year\n\nChoose growth over fear",
    "Discipline over excuses\n\nAnd progress over perfection",
    "Your time starts now",
    "New year",
"same dreams",
"stronger mindset",
"braver heart",
    "Happy New Year 🚀✨"
]

# ---------------- FRAME FUNCTION ----------------
def create_frame(text, bg_path):
    bg = Image.open(bg_path).convert("RGB").resize((W, H))
    
    # Optional: dark overlay for text visibility
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 120))
    bg = bg.convert("RGBA")
    bg = Image.alpha_composite(bg, overlay).convert("RGB")
    
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(FONT_FILE, 80)
    
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    x = (W - tw) // 2
    y = (H - th) // 2
    
    draw.multiline_text((x, y), text, fill="white", font=font, align="center")
    
    return np.array(bg)

# ---------------- CREATE CLIPS ----------------
clips = []
start = 0

for i, text in enumerate(texts):
    bg_path = BG_IMAGES[i % len(BG_IMAGES)]  # repeat if fewer backgrounds
    clip = (
        ImageClip(create_frame(text, bg_path))
        .set_duration(SLIDE_DURATION)
        .set_start(start)
        .fx(fadein, 0.4)
        .fx(fadeout, 0.4)
    )
    clips.append(clip)
    start += SLIDE_DURATION

# ---------------- AUDIO ----------------
BG_MUSIC = "assets/bg_music.wav"
audio_tracks = []

if os.path.exists(BG_MUSIC):
    audio_tracks.append(AudioFileClip(BG_MUSIC).volumex(0.2))

final_audio = CompositeAudioClip(audio_tracks) if audio_tracks else None

# ---------------- FINAL VIDEO ----------------
final = CompositeVideoClip(clips, size=(W, H))
if final_audio:
    final = final.set_audio(final_audio)

final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("✅ VIDEO CREATED: Each text has its own background")
