from enum import Enum, auto

class Event(Enum):          # Arguments

    NEW_FRAME = auto()
    UPDATE_GAME = auto()

    KEY_DOWN = auto()       # key
    KEY_UP = auto()         # key
    KEY_PRESSED = auto()    # key

    NEW_LEVEL = auto()      # level
    RESTART_LEVEL = auto()
    RESET = auto()          # player, x, y
    LOAD_BINDS = auto()     # binds

    COLLISION_X = auto()    # entity, rect
    COLLISION_Y = auto()    # entity, rect
    
    INTERACTION = auto()    # uuid, player
    DEATH = auto()          # player
    USE = auto()            # player