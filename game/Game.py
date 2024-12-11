
from utils import Subject, Event, Locator, EventsQ
from entities import Character, Menu, LevelManager, Transition
from game.consts import DISPLAY_W, DISPLAY_H, SCALE

class Game(Subject):
    
    def __init__(self):
        super().__init__()
        self.set_display_size(DISPLAY_W, DISPLAY_H)
        self.fps = 60
        self.menu = Menu(self)
        self.paused = True

        self.register_events(
            Event.UPDATE_GAME
        )

        Locator.add(Character(1, x=0, y=0, scale=SCALE))
        Locator.add(Character(2, x=0, y=0, scale=SCALE))
        self.level_manager = LevelManager()
        self.transition = Transition()


    def on_update_game(self):
        self.move_players()
        self.check_interactables()


    def move_players(self):
        for player in Locator.get(Character):
            player.move_y()
            self.collisions_y(player)
            player.move_x()
            self.collisions_x(player)


    def collision_rect(self, player):
        hitbox_rect = player.get_hitbox_rect()
        for rect in Locator.get_collidables():
            if hitbox_rect.colliderect(rect):
                return rect
    

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


    def draw(self):
        self.level_manager.draw(self.display)
        self.menu.draw(self.display)
        self.transition.draw(self.display)