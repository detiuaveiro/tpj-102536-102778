import pygame

from utils import Entity
from sprites import Fluid as FluidSprite


class Fluid(Entity):
    def __init__(self, fluid_type):
        super().__init__()
        self.fluid_type = fluid_type
        self.sprites_group = pygame.sprite.Group()


    def add(self, image, x, y):
        fluid = FluidSprite(image, x, y)
        self.sprites_group.add(fluid)


    def get_rects(self):
        return [sprite.hitbox_rect for sprite in self.sprites_group]

    
    def draw(self, screen):
        self.sprites_group.draw(screen)
