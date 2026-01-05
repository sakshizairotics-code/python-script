from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import VideoClip, AudioFileClip, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout

# ---------------- CONFIG ----------------
W, H = 1080, 1920
FPS = 20
DURATION = 16

FONT_FILE = "C:/Windows/Fonts/seguiemj.ttf"
BG_IMAGE = "assets/bg6.jpg"
BG_MUSIC = "assets/bg_music.wav"
OUTPUT = "newfeature.mp4"

FONT_SIZE = 64

# ---------------- FRAME FUNCTION ----------------
def create_frame(text, t):
    img = Image.open(BG_IMAGE).convert("RGB").resize((W, H))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    # slide-up animation
    y_offset = int(250 - t * 80)

    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (W - text_w) // 2
    y = (H - text_h) // 2 + y_offset

    draw.multiline_text((x, y), text, font=font, fill="white", align="center")
    return np.array(img)

# ---------------- ANIMATED CLIP ----------------
def animated_text_clip(text, start_time):
    clip = VideoClip(
        lambda t: create_frame(text, t),
        duration=4
    ).set_fps(FPS)

    clip = fadein(clip, 0.4)
    clip = fadeout(clip, 0.4)
    return clip.set_start(start_time)

# ---------------- TEXT ----------------
text1 = "EVs are computers\n\nthat happen\n\nto have wheels ⚡"
text2 = "Every drive\n\ngenerates data 📊\n\nLearning machines"
text3 = "Cleaner streets\n\nCleaner grids 🌱"
text4 = "Future cars\n\nwill calculate 🤖"

# ---------------- CLIPS ----------------
clip1 = animated_text_clip(text1, 0)
clip2 = animated_text_clip(text2, 4)
clip3 = animated_text_clip(text3, 8)
clip4 = animated_text_clip(text4, 12)

# ---------------- AUDIO ----------------
audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION)

# ---------------- FINAL VIDEO ----------------
final = CompositeVideoClip(
    [clip1, clip2, clip3, clip4],
    size=(W, H)
).set_audio(audio)

final.write_videofile(
    OUTPUT,
    codec="libx264",
    audio_codec="aac",
    fps=FPS
)

print("✅ VIDEO CREATED SUCCESSFULLY (SLIDE-UP TEXT ANIMATION)")
