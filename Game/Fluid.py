import pygame
from utils import Entity


class FluidSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.hitbox_rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox_rect.centerx = self.rect.centerx
        self.hitbox_rect.bottom = self.rect.bottom


    def draw(self, screen):
        screen.blit(self.image, self.rect)



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
