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
DURATION = 15  # Total duration

BG_VIDEO = "assets/bg_video.mp4"
BG_MUSIC = "assets/sbg_music.wav"
OUTPUT = "output_multi_text.mp4"

FONT_FILE = "C:/Windows/Fonts/arial.ttf"
FONT_SIZE = 64
TEXT_COLOR = "yellow"
SHADOW_COLOR = "black"

# ---------- MULTIPLE TEXT SLIDES ----------
TEXTS = [
    "finally the farewell\n\ncall has come from swami\n\nits time to go to akkalkot",
    "all devotees’ service 🙇🏼‍♀️\n\nlearned from swami 🙏🏼",
    "take the sacred legacy ❤️\n\nof Akkalkot with you 🙇🏼‍♀️",
    "devotion, faith & loyalty 🙏🏼💗\n\nwith swami's blessings 🙇🏼‍♀️"
]

SLIDE_DURATION = DURATION / len(TEXTS)  # Split total duration

# ---------- CHECK FILES ----------
if not os.path.exists(BG_VIDEO):
    raise FileNotFoundError(f"Background video not found: {BG_VIDEO}")
if not os.path.exists(BG_MUSIC):
    raise FileNotFoundError(f"Background music not found: {BG_MUSIC}")

# ---------- LOAD BACKGROUND VIDEO ----------
bg_clip = VideoFileClip(BG_VIDEO).subclip(0, DURATION)
bg_clip = bg_clip.resize((WIDTH, HEIGHT))

# ---------- FUNCTION TO DRAW TEXT WITH SHADOW ----------
def make_text_frame(text):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
    
    # Calculate position
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    # Shadow + text
    draw.multiline_text((x+2, y+2), text, font=font, fill=SHADOW_COLOR, align="center")
    draw.multiline_text((x, y), text, font=font, fill=TEXT_COLOR, align="center")
    
    return np.array(img)

# ---------- CREATE MULTIPLE TEXT CLIPS ----------
text_clips = []
for i, t in enumerate(TEXTS):
    clip = ImageClip(make_text_frame(t)).set_duration(SLIDE_DURATION)
    clip = fadein(clip, 0.5).fadeout(0.5)
    clip = clip.set_start(i * SLIDE_DURATION)
    text_clips.append(clip)

# ---------- DIM BACKGROUND FOR TEXT READABILITY ----------
def dim_frame(get_frame, t):
    frame = get_frame(t)
    return (frame * 0.6).astype(np.uint8)  # Darken 40%
dim_bg_clip = bg_clip.fl(dim_frame)

# ---------- LOAD AUDIO ----------
audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION)

# ---------- COMBINE VIDEO + TEXT + AUDIO ----------
final = CompositeVideoClip([dim_bg_clip, *text_clips]).set_audio(audio)

# ---------- EXPORT ----------
final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Multi-text video created successfully with dimmed background, fade effect, and audio")
