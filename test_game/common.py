from enum import Enum, auto


class Directions(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class States(Enum):
    IDLE = 'idle'
    WALK = 'walk'
    JUMP = 'jump'
    DEATH = 'death'
    RUN = 'run'