import pygame

from utils import Entity, Event, Sound
from game.consts import DISPLAY_W, DISPLAY_H


class Transition(Entity):

    def __init__(self):
        self.active = True
        self.radius = 0
        self.max_radius = DISPLAY_W
        self.surface = pygame.Surface((DISPLAY_W, DISPLAY_H), pygame.SRCALPHA)

        self.register_events(
            Event.NEW_LEVEL,
            Event.RESTART_LEVEL,
            Event.UPDATE_GAME
        )
        self.register_paused_events(
            Event.NEW_LEVEL,
            Event.RESTART_LEVEL,
            Event.UPDATE_GAME,
        )


    def start(self):
        self.active = True
        self.radius = 0
        Sound.play_sound('transition')


    def on_new_level(self, level):
        self.start()


    def on_restart_level(self):
        self.start()


    def on_paused_new_level(self):
        self.start()


    def on_paused_restart_level(self):
        self.start()


    def on_paused_update_game(self):
        self.on_update_game()


    def on_update_game(self):
        if not self.active:
            return

        self.radius += 20
        if self.radius >= self.max_radius:
            self.active = False


    def draw(self, display):
        if not self.active:
            return
        pygame.draw.circle(self.surface, (0, 0, 0, 255), (DISPLAY_W// 2, DISPLAY_H // 2), self.max_radius)
        pygame.draw.circle(self.surface, (0, 0, 0, 0), (DISPLAY_W// 2, DISPLAY_H // 2), self.radius)
        display.blit(self.surface, (0, 0))