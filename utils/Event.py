from enum import Enum, auto

class Event(Enum):
    NEW_FRAME = auto()
    UPDATE_GAME = auto()
    KEY_DOWN = auto()
    KEY_UP = auto()
    KEY_PRESSED = auto()
    MOVE_RIGHT = auto()
    MOVE_LEFT = auto()
    JUMP = auto()
    ON_GROUND = auto()
    NONE = auto()
