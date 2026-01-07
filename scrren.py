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
SLIDE_DURATION = 4
FONT_FILE = "C:/Windows/Fonts/seguiemj.ttf"
OUTPUT = "auto_reel_final.mp4"

# Background images
BG_IMAGES = [
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg9.jpg",
    "assets/bg8.jpg"
]

# Multi-line text for slides
texts = [
    ["This year", "Choose growth over fear"],
    ["Discipline over excuses", "And progress over perfection"],
    ["Your time starts now"],
    ["Happy New Year 🚀✨"]
]

# Background music
BG_MUSIC = "assets/bg_music.wav"

# ---------------- CREATE FRAME FUNCTION ----------------
def create_frame(text_lines, bg_path, zoom=1.0):
    # Load background and apply zoom
    base = Image.open(bg_path).convert("RGB")
    Wz, Hz = int(W*zoom), int(H*zoom)
    bg = base.resize((Wz, Hz), Image.Resampling.LANCZOS)

    # Crop center
    left = (Wz - W)//2
    top = (Hz - H)//2
    bg = bg.crop((left, top, left+W, top+H))

    # Dark overlay for text visibility
    overlay = Image.new("RGBA", (W, H), (0,0,0,120))
    bg = bg.convert("RGBA")
    bg = Image.alpha_composite(bg, overlay).convert("RGB")

    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(FONT_FILE, 80)

    # Draw each line centered
    total_height = 0
    line_heights = []
    for line in text_lines:
        bbox = draw.multiline_textbbox((0,0), line, font=font, align="center")
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height + 20

    y = (H - total_height) // 2
    for i, line in enumerate(text_lines):
        bbox = draw.multiline_textbbox((0,0), line, font=font, align="center")
        tw = bbox[2]-bbox[0]
        x = (W - tw)//2
        draw.multiline_text((x, y), line, fill="white", font=font, align="center")
        y += line_heights[i] + 20

    return np.array(bg)

# ---------------- CREATE CLIPS ----------------
clips = []
start = 0

for i, text_lines in enumerate(texts):
    bg_path = BG_IMAGES[i % len(BG_IMAGES)]

    # Create ImageClip
    clip = (
        ImageClip(create_frame(text_lines, bg_path))
        .set_duration(SLIDE_DURATION)
        .set_start(start)
        .fx(fadein, 0.5)
        .fx(fadeout, 0.5)
        # Ken Burns zoom effect
        .resize(lambda t: 1 + 0.02*t)
        .set_position(("center","center"))
    )
    clips.append(clip)
    start += SLIDE_DURATION

# ---------------- ADD AUDIO ----------------
audio_tracks = []
if os.path.exists(BG_MUSIC):
    audio_tracks.append(AudioFileClip(BG_MUSIC).volumex(0.2))
final_audio = CompositeAudioClip(audio_tracks) if audio_tracks else None

# ---------------- FINAL VIDEO ----------------
final = CompositeVideoClip(clips, size=(W,H))
if final_audio:
    final = final.set_audio(final_audio)

final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("✅ VIDEO CREATED: Multi-line + Zoom + Fade effect")
