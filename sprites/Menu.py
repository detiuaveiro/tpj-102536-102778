import pygame
from pygame.sprite import Sprite

from game.consts import MENU_BOX_SIZE


class MenuSprite(Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((800, 600), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (500, 350)
        self.options: list[tuple[str, callable]] = [] # list of options
        self.selected: int = 0 # selected option
        self.positions: list[tuple[int, int]] = [] # positions of options
        self.mapping: list[list[int]] = [] # mapping of options
        self.pos: tuple[int, int] = (0, 0) # mapping matrix index
        self.title: str = "" # title of the menu


    def handle_key(self, key, draw=True):
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
        if draw:
            self.draw_options()


    def draw_text(self, text, size, pos, b):
        font = pygame.font.Font(None, size)
        text_color = pygame.Color("white")
        border_color = pygame.Color("black")
        text_ = font.render(text, True, text_color)
        text_rect = text_.get_rect(center=pos)
        for dx, dy in [(-b, 0), (b, 0), (0, -b), (0, b), (-b, -b), (-b, b), (b, -b), (b, b)]:
            border = font.render(text, True, border_color)
            border_rect = text_rect.copy()
            border_rect.move_ip(dx, dy)
            self.image.blit(border, border_rect)
        self.image.blit(text_, text_rect)


    def draw_title(self):
        self.draw_text(self.title, 72, (400, 50), 3)


    def draw_options(self):
        self.draw_title()
        colors = ["white" if i != self.selected else "green" for i in range(len(self.options))]
        for option, color, pos in zip(self.options, colors, self.positions):
            text = pygame.font.Font(None, 36).render(option[0], True, pygame.Color(color))
            text_rect = text.get_rect(center=pos)
            box_rect = pygame.Rect(pos[0] - MENU_BOX_SIZE[0] // 2, pos[1] - MENU_BOX_SIZE[1] // 2, MENU_BOX_SIZE[0], MENU_BOX_SIZE[1])
            pygame.draw.rect(self.image, pygame.Color("black"), box_rect)
            pygame.draw.rect(self.image, pygame.Color(color), box_rect, 2)
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
        self.positions = [ (400, 200 + 70*i) for i in range(4) ]
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
        self.positions = [ (400, 170 + 70*i) for i in range(5) ]
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
        self.positions = [ (400, 200 + 70 * i) for i in range(len(self.levels) + 1) ]
        self.draw_options()


class SettingsMenu(MenuSprite):
     
    def __init__(self, menu):
        super().__init__()
        self.title = "Settings Menu"
        self.menu = menu
        self.load_options()
        self.mapping = [
            [0, 1],
            [2, 7],
            [3, 8],
            [4, 9],
            [5, 10],
            [6, 11],
            [12, 12]
        ]

        self.positions = [ (250, 130), (550, 130) ] + [ (200, 240 + 50 * i) for i in range(5) ] + [ (600, 240 + 50 * i) for i in range(5) ] + [ (400, 530) ]
        self.draw_options()


    def load_options(self):
        self.options = [
            ("Load", self.menu.load_controls),
            ("Save", self.menu.save_controls),

            (f"left: {self.get_name(self.menu.settings_[0]['left'])}", self.menu.controls),
            (f"right: {self.get_name(self.menu.settings_[0]['right'])}", self.menu.controls),
            (f"jump: {self.get_name(self.menu.settings_[0]['jump'])}", self.menu.controls),
            (f"sprint: {self.get_name(self.menu.settings_[0]['sprint'])}", self.menu.controls),
            (f"use: {self.get_name(self.menu.settings_[0]['use'])}", self.menu.controls),
            
            (f"left: {self.get_name(self.menu.settings_[1]['left'])}", self.menu.controls),
            (f"right: {self.get_name(self.menu.settings_[1]['right'])}", self.menu.controls),
            (f"jump: {self.get_name(self.menu.settings_[1]['jump'])}", self.menu.controls),
            (f"sprint: {self.get_name(self.menu.settings_[1]['sprint'])}", self.menu.controls),
            (f"use: {self.get_name(self.menu.settings_[1]['use'])}", self.menu.controls),
            
            ("Back", self.menu.back)
        ]


    def handle_key(self, key, draw=True):
        bind = self.options[self.selected][0].split(":")[0]
        if self.menu.chosing_bind:
            player = 0 if self.selected < 6 else 1
            self.options[self.selected] = (f"{bind}: {self.get_name(key)}", self.menu.controls)
            self.menu.change_bind(player, bind, key)
        else:
            super().handle_key(key, draw=False)
            if key == pygame.K_RETURN:
                self.load_options()
                if self.selected not in (0,1,12):
                    self.options[self.selected] = (f"{bind}: [press key]", self.menu.controls)
            elif key == None:
                self.options[self.selected] = (f"{bind}: {self.get_name(self.menu.settings_[0][bind])}", self.menu.controls)
        self.draw_options()


    def draw_options(self):
        super().draw_options()
        for i, pos in enumerate([(200, 190), (600, 190)]):
            self.draw_text("Player " + str(i + 1), 36, pos, 2)

    def get_name(self, key):
        return pygame.key.name(key)