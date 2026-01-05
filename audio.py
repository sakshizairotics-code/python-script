from moviepy.audio.io.AudioFileClip import AudioFileClip

# -------- CONFIG --------
INPUT_AUDIO = r"C:\Users\Sakshi\Desktop\sonali\_.sonali._47_14020825_081317226.mp4"
OUTPUT_AUDIO = "song_15_sec.mp3"

START_TIME = 0      # start from beginning
DURATION = 15       # 15 seconds
# ------------------------

audio = AudioFileClip(INPUT_AUDIO)

clip = audio.subclipped(START_TIME, START_TIME + DURATION)

clip.write_audiofile(
    OUTPUT_AUDIO,
    codec="mp3"
)

print("✅ 15 second audio created: swag_15_sec.mp3")
