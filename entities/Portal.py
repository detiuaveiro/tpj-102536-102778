import pygame

from utils import Entity, Event, Locator, EventsQ
from sprites import Portal as PortalSprite


class Portal(Entity):
    
    def __init__(self):
        super().__init__()
        self.sprites_group = pygame.sprite.Group()
        self.players_in = [False, False]
        self.players_using = [False, False]
        self.entered = False

        self.register_events(
            Event.UPDATE_GAME,
            Event.INTERACTION,
            Event.USE
        )


    def add(self, image, x, y):
        block = PortalSprite(image, x, y)
        self.sprites_group.add(block)
        Locator.add_interactable(self, block.rect)


    def on_update_game(self):
        self.players_in = [False, False]
        self.players_using = [False, False]


    def on_use(self, player):
        self.players_using[player - 1] = True
    

    def on_interaction(self, uuid, player):
        if self.id == uuid:
            self.players_in[player - 1] = True

            if all(self.players_in) and all(self.players_using) and not self.entered:
                self.entered = True
                EventsQ.add(Event.NEW_LEVEL, level=None)


    def get_rects(self):
        return [sprite.rect for sprite in self.sprites_group]


    def draw(self, screen):
        self.sprites_group.draw(screen)
