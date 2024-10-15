from pygame.sprite import Sprite

from Utils import Observer


class Entity(Observer, Sprite):

    def __init__(self):
        Observer.__init__(self)
        Sprite.__init__(self)
