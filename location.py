from PIL import Image, ImageDraw, ImageFont
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
FONT_FILE = "assets/nirmala.ttf"
FONT_SIZE = 64
OUTPUT = "marathi_location_correct.mp4"

MAIN_TEXT = """चला निरोप आलाय स्वामीनंचा 😇

जायला लागतं अक्कलकोटला 🙏🏼🙇🏼‍♀️"""
LOCATION_TEXT = "📍 अक्कलकोट, महाराष्ट्र"

TEXT_COLOR = "yellow"
SHADOW_COLOR = "black"

# ---------- CHECK FILES ----------
for f in [BG_VIDEO, BG_MUSIC, FONT_FILE]:
    if not os.path.exists(f):
        raise FileNotFoundError(f"❌ Missing file: {f}")

# ---------- LOAD BACKGROUND VIDEO ----------
bg_clip = VideoFileClip(BG_VIDEO).subclip(0, DURATION).resize((WIDTH, HEIGHT))

# ---------- MAIN TEXT IMAGE ----------
def make_main_text_frame(text):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
    
    bbox = draw.multiline_textbbox((0,0), text, font=font, align="center")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    draw.multiline_text((x+2, y+2), text, font=font, fill=SHADOW_COLOR, align="center")
    draw.multiline_text((x, y), text, font=font, fill=TEXT_COLOR, align="center")
    return np.array(img)

# ---------- LOCATION TEXT IMAGE (tight bounding box) ----------
def make_location_text_frame(text):
    font = ImageFont.truetype(FONT_FILE, int(FONT_SIZE*0.5))
    # Get text size
    dummy_img = Image.new("RGBA", (1,1))
    draw = ImageDraw.Draw(dummy_img)
    w, h = draw.textsize(text, font=font)

    # Create image just big enough for text
    img = Image.new("RGBA", (w+10, h+10), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.text((2,2), text, font=font, fill=SHADOW_COLOR)
    draw.text((0,0), text, font=font, fill="cyan")
    return np.array(img)

# ---------- CREATE CLIPS ----------
main_text_clip = ImageClip(make_main_text_frame(MAIN_TEXT)).set_duration(DURATION).set_position("center")
main_text_clip = fadein(main_text_clip, 1).fadeout(1)

location_clip = ImageClip(make_location_text_frame(LOCATION_TEXT)).set_duration(DURATION).set_position(("left","bottom"))
location_clip = fadein(location_clip, 1).fadeout(1)

# ---------- AUDIO ----------
audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION)

# ---------- COMBINE ----------
final = CompositeVideoClip([bg_clip, main_text_clip, location_clip]).set_audio(audio)

# ---------- EXPORT ----------
final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Marathi video with visible location created successfully!")
