import pygame
from pygame.sprite import Sprite
from utils import Entity, Event, EventsQ

SETTINGS = [
    {
        "left": pygame.K_a,
        "right": pygame.K_d,
        "jump": pygame.K_SPACE,
        "sprint": pygame.K_LSHIFT,
        "use": pygame.K_e,
    },
    {
        "left": pygame.K_a,
        "right": pygame.K_d,
        "jump": pygame.K_SPACE,
        "sprint": pygame.K_LSHIFT,
        "use": pygame.K_e,
    },
]


class MenuSprite(Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((800, 600))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.options: list[tuple[str, callable]] = [] # list of options
        self.selected: int = 0 # selected option
        self.positions: list[tuple[int, int]] = [] # positions of options
        self.mapping: list[list[int]] = [] # mapping of options
        self.pos: tuple[int, int] = (0, 0) # mapping matrix index
        self.title: str = "" # title of the menu


    def handle_key(self, key):
        if key == pygame.K_RIGHT:
            self.pos = (self.pos[0], (self.pos[1] + 1) % len(self.mapping[self.pos[0]]))
        elif key == pygame.K_LEFT:
            self.pos = (self.pos[0], (self.pos[1] - 1) % len(self.mapping[self.pos[0]]))
        elif key == pygame.K_DOWN:
            self.pos = ((self.pos[0] + 1) % len(self.mapping), self.pos[1])
        elif key == pygame.K_UP:
            self.pos = ((self.pos[0] - 1) % len(self.mapping), self.pos[1])
        elif key == pygame.K_RETURN:
            self.options[self.mapping[self.pos[0]][self.pos[1]]][1]()
        self.selected = self.mapping[self.pos[0]][self.pos[1]]
        self.draw_options()


    def draw_title(self):
        title = pygame.font.Font(None, 72).render(self.title, True, pygame.Color("white"))
        title_rect = title.get_rect(center=(400, 50))
        self.image.blit(title, title_rect)


    def draw_options(self):
        self.image.fill("black")
        self.draw_title()
        colors = ["white" if i != self.selected else "green" for i in range(len(self.options))]
        for option, color, pos in zip(self.options, colors, self.positions):
            text = pygame.font.Font(None, 36).render(option[0], True, pygame.Color(color))
            text_rect = text.get_rect(center=pos)
            self.image.blit(text, text_rect)


    def draw(self, display):
        display.blit(self.image, self.rect)


class HomeMenu(MenuSprite):
        
    def __init__(self, menu):
        super().__init__()
        self.title = "Home Menu"
        self.options = [
            ("Start", menu.start),
            ("Levels", menu.levels),
            ("Settings", menu.settings),
            ("Exit", menu.exit)
        ]
        self.mapping = [[0], [1], [2], [3]]
        self.positions = [ (400, 150), (400, 200), (400, 250), (400, 300) ]
        self.draw_options()


class GameMenu(MenuSprite):
    
    def __init__(self, menu):
        super().__init__()
        self.title = "Game Menu"
        self.options = [
            ("Resume", menu.resume),
            ("Restart", menu.restart),
            ("Levels", menu.levels),
            ("Settings", menu.settings),
            ("Exit", menu.exit)
        ]
        self.mapping = [[0], [1], [2], [3], [4]]
        self.positions = [ (400, 150), (400, 200), (400, 250), (400, 300), (400, 350) ]
        self.draw_options()


class LevelsMenu(MenuSprite):
     
    def __init__(self, menu):
        super().__init__()
        self.title = "Levels Menu"
        self.levels = ["Level 1", "Level 2", "Level 3"]
        self.options = [
            (level, lambda level=level: menu.level(int(level[-1]))) for level in self.levels
        ] + [("Back", menu.back)]
        self.mapping = [[i] for i in range(len(self.levels))] + [[len(self.levels)]]
        self.positions = [ (400, 150 + 50 * i) for i in range(len(self.levels) + 1) ]
        self.draw_options()


class SettingsMenu(MenuSprite):
     
    def __init__(self, menu):
        super().__init__()
        self.title = "Settings Menu"
        self.menu = menu
        self.options = [
            ("Load", menu.load_controls),
            ("Save", menu.save_controls),

            (f"left: {pygame.key.name(SETTINGS[0]['left'])}", menu.controls),
            (f"right: {pygame.key.name(SETTINGS[0]['right'])}", menu.controls),
            (f"jump: {pygame.key.name(SETTINGS[0]['jump'])}", menu.controls),
            (f"sprint: {pygame.key.name(SETTINGS[0]['sprint'])}", menu.controls),
            (f"use: {pygame.key.name(SETTINGS[0]['use'])}", menu.controls),
            
            (f"left: {pygame.key.name(SETTINGS[1]['left'])}", menu.controls),
            (f"right: {pygame.key.name(SETTINGS[1]['right'])}", menu.controls),
            (f"jump: {pygame.key.name(SETTINGS[1]['jump'])}", menu.controls),
            (f"sprint: {pygame.key.name(SETTINGS[1]['sprint'])}", menu.controls),
            (f"use: {pygame.key.name(SETTINGS[1]['use'])}", menu.controls),
            
            ("Back", menu.back)
        ]
        self.mapping = [
            [0, 1],
            [2, 7],
            [3, 8],
            [4, 9],
            [5, 10],
            [6, 11],
            [12, 12]
        ]

        self.positions = [ (300, 100), (500, 100) ] + [ (200, 200 + 50 * i) for i in range(5) ] + [ (600, 200 + 50 * i) for i in range(5) ] + [ (400, 450) ]
        self.draw_options()


    def handle_key(self, key):
        bind = self.options[self.selected][0].split(":")[0]
        if self.menu.chosing_bind:
            player = 0 if self.selected < 6 else 1
            self.options[self.selected] = (f"{bind}: {pygame.key.name(key)}", self.menu.controls)
            self.menu.change_bind(player, bind, key)
        else:
            if key == pygame.K_RETURN and self.selected not in (0,1,12):
                self.options[self.selected] = (f"{bind}: [press key]", self.menu.controls)
            elif key == None:
                self.options[self.selected] = (f"{bind}: {pygame.key.name(SETTINGS[0][bind])}", self.menu.controls)
            super().handle_key(key)
        self.draw_options()

    def draw_options(self):
        super().draw_options()
        for i, pos in enumerate([(200, 150), (600, 150)]):
            text = pygame.font.Font(None, 36).render(f"Player {i + 1}", True, pygame.Color("white"))
            text_rect = text.get_rect(center=(pos[0], pos[1]))
            self.image.blit(text, text_rect)


class Menu(Entity):

    def __init__(self, game):
        super().__init__()
        self.register_paused_events(
            Event.KEY_DOWN
        )
        self.register_events(
            Event.KEY_DOWN
        )
        self.game = game
        self.menus = [HomeMenu(self)]
        self.chosing_bind = False


    def on_paused_key_down(self, key):
        if key == pygame.K_ESCAPE:
            if self.chosing_bind:
                self.chosing_bind = False
                self.menus[-1].handle_key(None)
            elif not isinstance(self.menus[-1], HomeMenu):
                self.menus.pop()
        else:
            self.menus[-1].handle_key(key)
        if len(self.menus) == 0:
            self.game.paused = False


    def on_key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.menus = [GameMenu(self)]
            self.game.paused = True


    def draw(self, display):
        if self.menus:
            self.menus[-1].draw(display)


    def start(self):
        self.menus = []

    def restart(self):
        self.menus = []

    def resume(self):
        self.menus = []

    def level(self, level):
        self.menus = []
        EventsQ.add(Event.NEW_LEVEL, level=level)

    def levels(self):
        self.menus.append(LevelsMenu(self))

    def settings(self):
        self.menus.append(SettingsMenu(self))

    def back(self):
        self.menus.pop()

    def exit(self):
        self.game.running = False

    def load_controls(self):
        ...

    def save_controls(self):
        ...

    def controls(self):
        print("Chosing bind")
        self.chosing_bind = True

    def change_bind(self, player, bind, new_key):
        print(f"Changed {player} {bind} {new_key}")
        SETTINGS[player][bind] = new_key
        self.chosing_bind = False