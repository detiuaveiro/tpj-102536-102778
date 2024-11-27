from enum import Enum, auto

class Event(Enum):

    NEW_FRAME = auto()
    UPDATE_GAME = auto()

    KEY_DOWN = auto()
    KEY_UP = auto()
    KEY_PRESSED = auto()

    NEW_LEVEL = auto()

    COLLISION_X = auto()
    COLLISION_Y = auto()
