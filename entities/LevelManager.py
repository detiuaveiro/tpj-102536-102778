import pygame

from utils import Entity, Event, Locator, EventsQ
from entities import Map, Character
from game.consts import MAP_FOLDER, SCALE, DISPLAY_W, DISPLAY_H, TRESHOLD


class LevelManager(Entity):

    def __init__(self):
        super().__init__()
        self.level = 1
        self.map = None
        self.map_width = None
        self.map_height = None
        self.map_rects = None
        self.surface = None
        self.surface_rect = None
        self.on_new_level(self.level)
        self.register_events(
            Event.NEW_LEVEL,
            Event.RESTART_LEVEL,
            Event.UPDATE_GAME,
        )


    def on_new_level(self, level):
        Locator.clear()
        self.level = level if level else self.level + 1
        self.map = Map(f"{MAP_FOLDER}/{self.level}", scale=SCALE)
        self.map_width, self.map_height = self.map.get_map_size()
        self.map_rects = self.map.get_rects()
        self.surface = pygame.Surface((DISPLAY_W, self.map_height))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.y = DISPLAY_H - self.map_height

        for i, (x, y) in enumerate(self.map.get_players_start()):
            EventsQ.add(Event.RESET, player=i+1, x=x, y=y)


    def on_restart_level(self):
        self.on_new_level(self.level)


    def on_update_game(self):
        pivot_player = Locator.get(Character)[0]
        hitbox = pivot_player.get_hitbox_rect()
        absolute_y = hitbox.y + self.surface_rect.y

        if absolute_y < TRESHOLD - hitbox.h and self.surface_rect.y < 0:
            self.surface_rect.y += abs(pivot_player.vel_y)
        elif absolute_y > DISPLAY_H - TRESHOLD and self.surface_rect.y > DISPLAY_H - self.map_height:
            self.surface_rect.y -= abs(pivot_player.vel_y)


    def draw(self, display):
        self.map.draw(self.surface)
        for player in Locator.get(Character):
            player.draw(self.surface)
        self.map.draw_fluids(self.surface)
        display.blit(self.surface, self.surface_rect)