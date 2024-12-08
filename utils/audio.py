import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


class AudioManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.enabled = pygame.mixer.get_num_channels() > 0
        self.is_muted = False

    @property
    def muted(self):
        return self.is_muted

    @muted.setter
    def muted(self, value):
        self.is_muted = value

    def play_audio(self, file, loop=True, stop_previous=False, volume=100, busy_check=False):
        if (not self.enabled or self.is_muted) or (busy_check and pygame.mixer.music.get_busy()):
            return
        if stop_previous:
            pygame.mixer.music.stop()

        pygame.mixer.music.load(f"audio/{file}.wav")
        pygame.mixer.music.set_volume(volume / 100)
        pygame.mixer.music.play(loops = -1 if loop else 0)

        while not pygame.mixer.music.get_busy():
            continue

    def stop_audio(self):
        if not self.enabled:
            return
        pygame.mixer.music.stop()
