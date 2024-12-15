import pygame

from utils import Entity, Event, Locator, EventsQ
from sprites import Fluid as FluidSprite
from game.consts import RESISTANCES


class Fluid(Entity):
    
    def __init__(self, fluid_type):
        super().__init__()
        self.fluid_type = fluid_type
        self.sprites_group = pygame.sprite.Group()

        self.register_events(
            Event.INTERACTION,
        )


    def add(self, image, x, y):
        fluid = FluidSprite(image, x, y)
        self.sprites_group.add(fluid)
        Locator.add_interactable(self, fluid.hitbox_rect)


    def get_rects(self):
        return [sprite.hitbox_rect for sprite in self.sprites_group]
    

    def on_interaction(self, uuid, player):
        if self.id == uuid and RESISTANCES[player-1] != self.fluid_type:
            EventsQ.add(Event.DEATH, player=player)


    def draw(self, screen):
        self.sprites_group.draw(screen)
