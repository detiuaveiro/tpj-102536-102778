import pygame
from pygame import Surface
from pygame.sprite import Sprite

from Utils import Event, Observer

import random
# set seed
random.seed(42)


class Food(Observer, Sprite):

    def __init__(self, color, width, height, scale):
        Observer.__init__(self)
        Sprite.__init__(self)
        self.color = color
        self.width = width
        self.height = height
        self.scale = scale

        self.position = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

        self.image = Surface((self.width * self.scale, self.height * self.scale), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.update()

        self.register_many(
            Event.EAT
        )


    def on_eat(self):
        self.position = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

    def update(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, self.color, (self.position[0] * self.scale, self.position[1] * self.scale, self.scale, self.scale))
        