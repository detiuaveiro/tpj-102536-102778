
from utils import Subject, Event, Locator, EventsQ
from entities import Character, Fluid, Mechanism, Menu, Map
from game.consts import DISPLAY_W, DISPLAY_H, MAP_FOLDER, SCALE
import pygame

SCROLL_THRESHOLD = 32   # tile_size * scale

class Game(Subject):
    
    def __init__(self):
        super().__init__()
        self.set_display_size(DISPLAY_W, DISPLAY_H)
        self.fps = 90
        self.menu = Menu(self)
        self.paused = True
        self.level = 1

        self.register_events(
            Event.UPDATE_GAME
        )

        # Map
        self.map = Map(MAP_FOLDER, scale=SCALE)
        self.map_rects = self.map.get_rects()
        self.bg_img = self.map.get_bg(DISPLAY_W, DISPLAY_H)

        Locator.add(Character(1, x=150, y=150, scale=SCALE))
        Locator.add(Character(2, x=800, y=300, scale=SCALE))


    def on_update_game(self):
        self.move_players()
        self.scroll()
        self.check_interactables()


    def move_players(self):
        for player in Locator.get(Character):
            player.move_y()
            self.collisions_y(player)
            player.move_x()
            self.collisions_x(player)


    def collision_rect(self, player):
        hitbox_rect = player.get_hitbox_rect()
        rects_idx = hitbox_rect.collidelistall(self.map_rects)
        if rects_idx:
            return self.map_rects[rects_idx[0]]
        
        barrier_rects = [r for m in Locator.get(Mechanism) for r in m.get_barrier_rects()]
        rects_idx = hitbox_rect.collidelistall(barrier_rects)
        if rects_idx:
            return barrier_rects[rects_idx[0]]
        
        return None
    

    def collisions_x(self, player):
        if rect := self.collision_rect(player):
            player.collide_x(rect)


    def collisions_y(self, player):
        if rect := self.collision_rect(player):
            player.collide_y(rect)


    def check_interactables(self):
        for player in Locator.get(Character):
            for uuid, rect in Locator.get_interactables():
                if player.get_hitbox_rect().colliderect(rect):
                    EventsQ.add(Event.INTERACTION, uuid=uuid, player=player.num)
    

    def scroll(self):
        pivot_player = Locator.get(Character)[0]
        hitbox = pivot_player.get_hitbox_rect()
        _, vel_y = pivot_player.get_vel()

        if hitbox.top < SCROLL_THRESHOLD and vel_y < 0:
            EventsQ.add(Event.SCROLL, uuid=pivot_player.id, limit=SCROLL_THRESHOLD, vel=vel_y)
            self.map.scroll(vel_y)

        elif hitbox.bottom > DISPLAY_H - SCROLL_THRESHOLD and vel_y > 0:
            EventsQ.add(Event.SCROLL, uuid=pivot_player.id, limit=DISPLAY_H - SCROLL_THRESHOLD, vel=vel_y)
            self.map.scroll(vel_y)


    def draw(self):
        self.display.blit(self.bg_img, (0, 0))
        self.map.draw(self.display)
        for player in Locator.get(Character):
            player.draw(self.display)
        self.map.draw_fluids(self.display)
        self.menu.draw(self.display)