from uuid import uuid4, UUID
from pygame.sprite import Sprite

from utils import Observer, FSM


class Entity(Observer):

    def __init__(self):
        super().__init__()
        self.id: UUID = uuid4()
        self.fsm: FSM = FSM()
        self.sprite: Sprite = None

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id
        return False


    def __hash__(self):
        return self.id.int
    

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"


