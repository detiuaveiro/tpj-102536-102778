from pygame.sprite import Sprite
from uuid import uuid4

from Utils import Observer, FSM


class Entity(Observer, Sprite):

    def __init__(self):
        Observer.__init__(self)
        Sprite.__init__(self)
        self.id = uuid4()
        self.fsm = FSM()


    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id
        return False


    def __hash__(self):
        return self.id.int
    

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"


