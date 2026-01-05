from moviepy.audio.io.AudioFileClip import AudioFileClip

audio = AudioFileClip(
    r"C:\Users\Sakshi\Desktop\sonali\_.sonali._47_14020825_081317226.mp4"
)

audio.subclipped(0, 5).write_audiofile("check_audio.mp3")
print("done")
