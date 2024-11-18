from enum import Enum, auto

class States(Enum):
    IDLE = 'idle'
    JUMPING = 'jumping'
    DEATH = 'death'
    RUNNING = 'running'