from enum import Enum, auto

class Event(Enum):
    NEW_FRAME = auto()
    UPDATE_GAME = auto()
    KEY_PRESSED = auto()