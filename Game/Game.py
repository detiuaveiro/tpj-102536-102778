
from utils import Subject, Event, Locator
from entities import Character, Fluid, Mechanism, Menu, Map
from game.consts import DISPLAY_W, DISPLAY_H, MAP_FOLDER, SCALE


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

        # Players
        self.player_1 = Character(1, x=800, y=200, scale=SCALE)
        self.player_2 = Character(2, x=800, y=300, scale=SCALE)
        self.players = [self.player_1, self.player_2]

        # Fluids
        self.water = Locator.get(Fluid)
        self.lava = Locator.get(Fluid)

        # Mechanisms
        self.mechanisms = Locator.get(Mechanism)
    

    def on_update_game(self):
        self.move_players()
        self.check_mechanisms()
    

    def move_players(self):
        for player in self.players:
            player.move_x()
            self.collisions_x(player)
            player.move_y()
            self.collisions_y(player)


    def collision_rect(self, player):
        hitbox_rect = player.get_hitbox_rect()
        rects_idx = hitbox_rect.collidelistall(self.map_rects)
        if rects_idx:
            return self.map_rects[rects_idx[0]]
        
        barrier_rects = [r for m in self.mechanisms for r in m.get_barrier_rects()]
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


    def check_mechanisms(self):
        for mechanism in self.mechanisms:
            trigger_rects = mechanism.get_trigger_rects()
            if self.trigger_collision(trigger_rects):
                mechanism.activate()
            else:
                mechanism.deactivate()


    def trigger_collision(self, trigger_rects):
        for player in self.players:
            hitbox = player.get_hitbox_rect()
            if hitbox.collidelistall(trigger_rects):
                return True
        return False
    

    def draw(self):
        self.display.blit(self.bg_img, (0, 0))
        self.map.draw(self.display)
        for player in self.players:
            player.draw(self.display)
        self.map.draw_fluids(self.display)
        self.menu.draw(self.display)
