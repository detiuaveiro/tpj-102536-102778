from enum import Enum, auto

class Event(Enum):
    UPDATE_GAME = auto()
    KEY_PRESSED = auto()
    # Snake
    EAT = auto()