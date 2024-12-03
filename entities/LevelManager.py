import pygame

from utils import Entity, Event, Locator
from entities import Map, Character
from game.consts import MAP_FOLDER, SCALE, DISPLAY_W, DISPLAY_H, TRESHOLD


class LevelManager(Entity):

    def __init__(self):
        super().__init__()
        self.level = 0
        self.map = None
        self.map_rects = None
        self.bg_img = None
        self.surface = None
        self.surface_rect = None
        self.on_new_level(self.level)
        self.register_events(
            Event.NEW_LEVEL,
            Event.RESTART_LEVEL,
            Event.UPDATE_GAME,
        )


    def on_new_level(self, level):
        self.level = level
        self.map = Map(MAP_FOLDER, scale=SCALE)
        self.map_rects = self.map.get_rects()
        self.bg_img = self.map.get_bg(DISPLAY_W, DISPLAY_H)
        self.surface = pygame.Surface((DISPLAY_W, 1500))
        self.surface_rect = self.surface.get_rect()


    def on_restart_level(self):
        self.on_new_level(self.level)


    def on_update_game(self):
        pivot_player = Locator.get(Character)[0]
        hitbox = pivot_player.get_hitbox_rect()
        absolute_y = hitbox.y + self.surface_rect.y
        if absolute_y < TRESHOLD - hitbox.h:
            self.surface_rect.y += abs(pivot_player.vel_y)
        elif absolute_y > DISPLAY_H - TRESHOLD:
            self.surface_rect.y -= abs(pivot_player.vel_y)


    def draw(self, display):
        self.surface.fill("black")
        self.map.draw(self.surface)
        for player in Locator.get(Character):
            player.draw(self.surface)
        self.map.draw_fluids(self.surface)
        display.blit(self.surface, self.surface_rect)