from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os, sys

WIDTH, HEIGHT = 1080, 1920
DURATION = 15

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

BG_IMAGE = os.path.join(ASSETS, "bg6.jpg")
BG_MUSIC = os.path.join(ASSETS, "bg_music.wav")
OUTPUT = os.path.join(BASE_DIR, "ev_fact_15sec.mp4")

if not os.path.exists(BG_IMAGE):
    print("❌ Image missing")
    sys.exit()

if not os.path.exists(BG_MUSIC):
    print("❌ Music missing")
    sys.exit()

# ---------- FULL SCREEN BACKGROUND ----------
# ===== FORCE FULL IMAGE (STRETCH MODE) =====
img = Image.open(BG_IMAGE).convert("RGB")

# ⚠️ Direct resize (image stretch होईल)
img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)

BG_FIXED = os.path.join(BASE_DIR, "bg_fixed.jpg")
img.save(BG_FIXED)



# ---------- TEXT ----------
text = (
    "EVs don’t just save fuel.\n\n"
    "They save money, air,\n"
    "and the future.\n\n"
    "That’s real progress ⚡🌍"
)

txt_img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(txt_img)
font = ImageFont.truetype("arial.ttf", 64)

bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]

x = (WIDTH - w) // 2
y = (HEIGHT - h) // 2

draw.multiline_text((x, y), text, fill="white", font=font, align="center")

TEXT_IMG = os.path.join(BASE_DIR, "text.png")
txt_img.save(TEXT_IMG)

# ---------- VIDEO ----------
bg = ImageClip(BG_FIXED).set_duration(DURATION)
txt = ImageClip(TEXT_IMG).set_duration(DURATION)

audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION)

final = CompositeVideoClip([bg, txt]).set_audio(audio)

final.write_videofile(
    OUTPUT,
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("✅ VIDEO CREATED (FULL BACKGROUND + AUDIO)")
