import pygame
from pygame.sprite import Sprite
import tkinter as tk
from tkinter import filedialog
import json
from pathlib import Path

from utils import Entity, Event, EventsQ

FOLDER = "settings/"
BOX_SIZE = (250, 50)


class MenuSprite(Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((800, 600))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.rect.center = (500, 400)
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
            pygame.draw.rect(self.image, pygame.Color(color), (pos[0] - BOX_SIZE[0] // 2, pos[1] - BOX_SIZE[1] // 2, BOX_SIZE[0], BOX_SIZE[1]), 2)
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


    def handle_key(self, key):
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
            text = pygame.font.Font(None, 36).render(f"Player {i + 1}", True, pygame.Color("white"))
            text_rect = text.get_rect(center=(pos[0], pos[1]))
            self.image.blit(text, text_rect)


    def get_name(self, key):
        return pygame.key.name(key)


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
        self.settings_ = json.load(open(FOLDER + "current.json")) if Path(FOLDER + "current.json").exists() else json.load(open(FOLDER + "default.json"))


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
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            initialdir=FOLDER,
            title="Select file",
            filetypes=(("json files", "*.json"),)
        )
        if file_path:
            with open(file_path, "r") as f1, open(FOLDER + "current.json", "w") as f2:
                self.settings_ = json.load(f1)
                json.dump(self.settings_, f2)


    def save_controls(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(
            initialdir=FOLDER,
            title="Select file",
            filetypes=(("json files", "*.json"),)
        )
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.settings_, file)
                

    def controls(self):
        self.chosing_bind = True

    def change_bind(self, player, bind, new_key):
        self.settings_[player][bind] = new_key
        self.chosing_bind = False
        with open(FOLDER + "current.json", "w") as file:
            json.dump(self.settings_, file)