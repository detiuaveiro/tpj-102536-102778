
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    # check if is inverted
    def is_inverted(self, direction: "Direction") -> bool:
        return self.value[0] == -direction.value[0] and self.value[1] == -direction.value[1]