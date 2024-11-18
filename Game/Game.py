import pygame

from Game.Map import Map
from Game.Character import Character
from utils import Subject, Event

DISPLAY_W, DISPLAY_H = 960, 640
SCALE = 2
MAP_FOLDER = "Game/Maps/2"


class Game(Subject):
    
    def __init__(self):
        super().__init__()
        self.set_display_size(DISPLAY_W, DISPLAY_H)
        self.register_events(
            Event.UPDATE_GAME
        )

        # Map
        self.map = Map(MAP_FOLDER, scale=SCALE)
        self.map_rects = self.map.get_rects()
        self.bg_img = self.map.get_bg(DISPLAY_W, DISPLAY_H)

        # Players
        self.player_1 = Character('Pink Monster', x=800, y=200, scale=SCALE)
        self.player_2 = Character('Blue Monster', x=100, y=200, scale=SCALE)
        self.players = [self.player_1, self.player_2]
        
        self.player_1.register_keys(
            right = pygame.K_RIGHT,
            left = pygame.K_LEFT,
            jump = pygame.K_UP
        )

        self.player_2.register_keys(
            right = pygame.K_d,
            left = pygame.K_a,
            jump = pygame.K_w
        )


    def on_update_game(self):
        for player in self.players:
            player.move_x()
            self.collisions_x(player)
            player.move_y()
            self.collisions_y(player)


    def draw(self):
        self.display.blit(self.bg_img, (0, 0))
        self.map.draw(self.display)
        for player in self.players:
            player.draw(self.display)
        

    def collision_rect(self, player):
        hitbox_rect = player.get_hitbox_rect()
        rects_idx = hitbox_rect.collidelistall(self.map_rects)
        if rects_idx:
            return self.map_rects[rects_idx[0]]
        return None
    

    def collisions_x(self, player):
        if rect := self.collision_rect(player):
            player.collide_x(rect)


    def collisions_y(self, player):
        if rect := self.collision_rect(player):
            player.collide_y(rect)
