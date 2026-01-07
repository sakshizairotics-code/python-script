# ---------------- FIX FOR PIL 10+ ----------------
from PIL import Image
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# ---------------- IMPORTS ----------------
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout

# ---------------- CONFIG ----------------
W, H = 1080, 1920
FPS = 30
FONT_FILE = "C:/Windows/Fonts/seguiemj.ttf"
OUTPUT = "auto_reel_final1.mp4"

NORMAL_DURATION = 2        # fast slides
LAST_DURATION = 4          # CTA slide

# Background images
BG_IMAGES = [
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg8.jpg"
]

texts = [
    ["This year", "Choose growth over fear"],
    ["Discipline over excuses", "And progress over perfection"],
    ["Your time starts now"],
    ["Happy New Year 🚀✨"]
]

BG_MUSIC = "assets/bg_music.wav"

# ---------------- FRAME CREATOR ----------------
def create_frame(text_lines, bg_path, zoom=1.0):
    base = Image.open(bg_path).convert("RGB")
    Wz, Hz = int(W*zoom), int(H*zoom)
    bg = base.resize((Wz, Hz), Image.Resampling.LANCZOS)

    left = (Wz - W)//2
    top = (Hz - H)//2
    bg = bg.crop((left, top, left+W, top+H))

    overlay = Image.new("RGBA", (W, H), (0,0,0,120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(FONT_FILE, 80)

    total_h = 0
    heights = []

    for line in text_lines:
        bbox = draw.textbbox((0,0), line, font=font)
        h = bbox[3]-bbox[1]
        heights.append(h)
        total_h += h + 25

    y = (H - total_h)//2

    for i, line in enumerate(text_lines):
        bbox = draw.textbbox((0,0), line, font=font)
        w = bbox[2]-bbox[0]
        x = (W-w)//2
        draw.text((x,y), line, fill="white", font=font)
        y += heights[i] + 25

    return np.array(bg)

# ---------------- PROGRESS BAR ----------------
def progress_bar(total_time):
    def make_frame(t):
        img = np.zeros((H, W, 3), dtype=np.uint8)
        bar_w = int((t/total_time)*W)
        img[30:40, :bar_w] = (255,255,255)
        return img
    return VideoClip(make_frame, duration=total_time)

# ---------------- CREATE CLIPS ----------------
clips = []
start = 0

for i, text_lines in enumerate(texts):
    duration = LAST_DURATION if i == len(texts)-1 else NORMAL_DURATION
    bg_path = BG_IMAGES[i % len(BG_IMAGES)]

    clip = (
        ImageClip(create_frame(text_lines, bg_path))
        .set_duration(duration)
        .set_start(start)
        .fx(fadein, 0.3)
        .fx(fadeout, 0.3)
        .resize(lambda t: 1 + 0.03*t)   # smooth zoom
    )

    clips.append(clip)
    start += duration

TOTAL_TIME = start

# Progress bar
def progress_bar(total_time):
    def make_frame(t):
        img = np.zeros((H, W, 4), dtype=np.uint8)  # RGBA transparent
        bar_w = int((t / total_time) * W)

        # white bar
        img[30:40, :bar_w] = (255, 255, 255, 255)
        return img

    return (
        VideoClip(make_frame, duration=total_time)
        .set_position(("center", "top"))
    )


# ---------------- AUDIO ----------------
if os.path.exists(BG_MUSIC):
    audio = AudioFileClip(BG_MUSIC).subclip(0, TOTAL_TIME).volumex(0.25)
else:
    audio = None

# ---------------- FINAL VIDEO ----------------
final = CompositeVideoClip(clips, size=(W,H))
if audio:
    final = final.set_audio(audio)

final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Reel created with Progress Bar + CTA Timing")
