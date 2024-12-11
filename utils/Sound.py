import pygame
from time import time

from game.consts import SOUND_COOLDOWN, SOUNDS

class Sound:
    """
    Singleton class that manages the sounds in the game.

    Static Attributes
    -----------------
    _sounds (dict[str, int]): 
        Dictionary of sounds and their last played time.
    """

    _sounds: dict[str, int] = {}

    def __new__(cls) -> None:
        raise Exception("This class is a singleton.")
    

    @staticmethod
    def play_sound(name: str) -> None:
        """
        Play a sound.

        Parameters
        ----------
        name (str):
            Name of the sound.
        """
        path = SOUNDS[name]
        last = Sound._sounds.get(path, 0)
        now = time()
        if now - last > SOUND_COOLDOWN:
            Sound._sounds[path] = now
            pygame.mixer.Sound(path).play()
            