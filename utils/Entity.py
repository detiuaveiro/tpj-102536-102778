from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect
from uuid import uuid4, UUID

from utils import Observer, FSM


class Entity(Observer, Sprite):

    def __init__(self):
        Observer.__init__(self)
        Sprite.__init__(self)
        self.id: UUID = uuid4()
        self.fsm: FSM = FSM()
        self.image: Surface = None
        self.rect: Rect = None
        self.hitbox: Rect = None

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id
        return False


    def __hash__(self):
        return self.id.int
    

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"


