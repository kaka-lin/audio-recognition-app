import pygame
from pydub import AudioSegment

def play_mp3(fd):
    pygame.init()
    #pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load(fd)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(1.0)

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# need ffmpeg
def convert_mp3_to_wav(src, dst):
    print("Converting {} to {}".format(src, dst))
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
