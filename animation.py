from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ImageClip
from moviepy.video.fx import FadeIn, FadeOut

W, H = 1080, 1920
FPS = 30
DURATION = 5
FONT_FILE = "C:/Windows/Fonts/arial.ttf"
BG_IMAGE = "assets/bg1.jpg"

def create_frame():
    img = Image.open(BG_IMAGE).convert("RGB").resize((W, H))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT_FILE, 64)
    text = "Consistency is the key to success"

    w = font.getbbox(text)[2]
    h = font.getbbox(text)[3]
    x = (W - w) // 2
    y = (H - h) // 2

    draw.text((x, y), text, font=font, fill="white")
    return np.array(img)

def main():
    frame = create_frame()

    clip = (
        ImageClip(frame)
        .with_duration(DURATION)
        .with_fps(FPS)
        .with_effects([
            FadeIn(1),     # 🎬 fade in
            FadeOut(1)     # 🎬 fade out
        ])
    )

    clip.write_videofile(
        "output_animation.mp4",
        codec="libx264",
        audio=False,
        fps=FPS
    )

if __name__ == "__main__":
    main()
