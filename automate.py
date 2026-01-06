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
BG_IMAGE = "assets/bg8.jpg"
BG_MUSIC = "assets/bg_music.wav"
TEXT_FILE = "TEXT_FILE"
OUTPUT = "auto_reel.mp4"

# ---------------- AUTO CREATE TEXT FILE ----------------
if not os.path.exists(TEXT_FILE):
  with open(TEXT_FILE, "w", encoding="utf-8") as f:
    f.write(
        "This year\n\n"
        "Choose growth over fear\n\n"
        "Discipline over excuses\n\n"
        "And progress over perfection\n\n"
        "Your time starts now\n\n"
        "Happy New Year 🚀✨"
    )

# ---------------- LOAD TEXT ----------------
with open(TEXT_FILE, "r", encoding="utf-8") as f:
    texts = f.read().strip().split("\n\n")

# ---------------- OPTIONAL AI VOICE ----------------
voice_available = False
try:
    from gtts import gTTS
    tts = gTTS(" ".join(texts), lang="en")
    tts.save("voice.mp3")
    voice_available = True
except:
    print("⚠️ gTTS not installed – skipping voice")

# ---------------- FRAME FUNCTION (ZOOM SAFE) ----------------
def create_frame(text, zoom=1.06):
    base = Image.open(BG_IMAGE).convert("RGB")

    # zoom background safely (Pillow 10+ compatible)
    zw, zh = int(W * zoom), int(H * zoom)
    bg = base.resize((zw, zh), Image.Resampling.LANCZOS)

    # crop center
    left = (zw - W) // 2
    top = (zh - H) // 2
    bg = bg.crop((left, top, left + W, top + H))

    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(FONT_FILE, 90)

    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    x = (W - tw) // 2
    y = (H - th) // 2

    draw.multiline_text((x, y), text, fill="white", font=font, align="center")

    return np.array(bg)

# ---------------- CREATE CLIPS ----------------
clips = []
start = 0

for t in texts:
    clip = (
        ImageClip(create_frame(t))
        .set_duration(SLIDE_DURATION)
        .set_start(start)
        .fx(fadein, 0.4)
        .fx(fadeout, 0.4)
    )
    clips.append(clip)
    start += SLIDE_DURATION

# ---------------- AUDIO ----------------
audio_tracks = []

if os.path.exists(BG_MUSIC):
    audio_tracks.append(AudioFileClip(BG_MUSIC).volumex(0.2))

if voice_available:
    audio_tracks.append(AudioFileClip("voice.mp3"))

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

print("✅ REEL CREATED SUCCESSFULLY (NO PIL ERROR)")
