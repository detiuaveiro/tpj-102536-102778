import pygame
from time import time

from game.consts import SOUND_COOLDOWN, SOUNDS

class Sound:

    _sounds: dict[str, int] = {}

    @staticmethod
    def play_sound(name: str) -> None:
        path = SOUNDS[name]
        last = Sound._sounds.get(path, 0)
        now = time()
        if now - last > SOUND_COOLDOWN:
            Sound._sounds[path] = now
            pygame.mixer.Sound(path).play()
            