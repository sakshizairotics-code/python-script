from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout

# ---------------- CONFIG ----------------
W, H = 1080, 1920
FPS = 20
DURATION = 20

FONT_FILE = "C:/Windows/Fonts/seguiemj.ttf"
font = ImageFont.truetype(FONT_FILE, 64)
BG_IMAGE = "assets/bg7.jpg"
BG_MUSIC = "assets/sbg_music.wav"
OUTPUT = "swami_marathi.mp4"

# ---------------- FUNCTION ----------------
def create_frame(text):
    img = Image.open(BG_IMAGE).convert("RGB").resize((W, H))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, 64)
    

    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (W - w) // 2
    y = (H - h) // 2

    draw.multiline_text((x, y), text, font=font, fill="white", align="center")
    return np.array(img)

text1 = ("The message from Swami \n\n"
         "has come 😇Have to go to\n\n"
          " Akkalkot🙏🏼🙇🏼‍♀️")
text2 = ("Service of all devotees 🙇🏼‍♀️\n\n Taught by Swami 🙏🏼")
text3 = ("The sacred heritage of Akkalkot ❤️\n\n Take it with you 🙇🏼‍♀️")
text4 = ("Devotion, faith, and loyalty 🙏🏼💗\n\n With Swami’s blessings 🙇🏼‍♀️")




# ---------------- CLIPS ----------------
clip1 = fadeout(
    fadein(
        ImageClip(create_frame(text1))
        .set_duration(4)
        .set_fps(FPS),
        0.3
    ),
    0.3
).set_start(0)

clip2 = fadeout(
    fadein(
        ImageClip(create_frame(text2))
        .set_duration(4)
        .set_fps(FPS),
        0.3
    ),
    0.3
).set_start(4)

clip3 = fadeout(
    fadein(
        ImageClip(create_frame(text3))
        .set_duration(4)
        .set_fps(FPS),
        0.3
    ),
    0.3
).set_start(8)

clip4 = fadeout(
    fadein(
        ImageClip(create_frame(text4))
        .set_duration(4)
        .set_fps(FPS),
        0.3
    ),
    0.3
).set_start(12)


# ---------------- AUDIO ----------------
audio = AudioFileClip(BG_MUSIC).subclip(0, DURATION)

# ---------------- FINAL ----------------
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

print("✅ 15s VIDEO CREATED — 4 TEXTS DISPLAYED ONE BY ONE (FULL SCREEN)")
