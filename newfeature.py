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
OUTPUT = "newfeature_glow.mp4"

FONT_SIZE = 64
TEXT_COLOR = "white"
GLOW_COLOR = "black"

# ---------------- FRAME FUNCTION ----------------
def create_frame(text, t, global_t):
    img = Image.open(BG_IMAGE).convert("RGB").resize((W, H))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    # ---------------- Split text animation ----------------
    lines = text.split("\n")
    total_lines = len(lines)
    for i, line in enumerate(lines):
        # Each line moves from a slightly different direction
        y_offset = int(250 - t * 80) + i * 20
        # Optional: stagger animation slightly
        y_offset += int((i - total_lines/2) * 5 * (1 - t/4))

        bbox = draw.textbbox((0,0), line, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (W - text_w) // 2
        y = (H - text_h) // 2 + y_offset

        # ---------------- Glow / outline effect ----------------
        for offset in [(-3,-3), (-3,3), (3,-3), (3,3)]:  # shadow offsets
            draw.text((x+offset[0], y+offset[1]), line, font=font, fill=GLOW_COLOR)
        draw.text((x, y), line, font=font, fill=TEXT_COLOR)

        # ---------------- Moving underline ----------------
        underline_width = int((t/4) * text_w)  # grows with time
        underline_y = y + text_h + 10
        draw.rectangle([x, underline_y, x + underline_width, underline_y + 6], fill=TEXT_COLOR)

    # ---------------- Progress Bar ----------------
    progress = int((global_t / DURATION) * W)
    bar_height = 12
    draw.rectangle([0, H - bar_height, progress, H], fill="white")

    return np.array(img)

# ---------------- ANIMATED CLIP ----------------
def animated_text_clip(text, start_time):
    clip = VideoClip(
        lambda t: create_frame(text, t, t + start_time),
        duration=4
    ).set_fps(FPS)

    clip = fadein(clip, 0.4)
    clip = fadeout(clip, 0.4)
    return clip.set_start(start_time)

# ---------------- TEXT ----------------
text1 = "EVs are computers\n\n\nthat happen\n\n\nto have wheels"
text2 = "Every drive\n\n\ngenerates data\n\n\nLearning machines"
text3 = "Cleaner streets\n\n\nCleaner grids"
text4 = "Future cars\n\n\nwill calculate"

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

print("✅ VIDEO CREATED: slide-up + glow text + moving underline + split animation + progress bar")
