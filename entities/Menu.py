import pygame
import tkinter as tk
from tkinter import filedialog
import json

from utils import Entity, Event, EventsQ
from sprites import HomeMenu, GameMenu, LevelsMenu, SettingsMenu
from game.consts import SETTINGS, SETTINGS_FOLDER

BOX_SIZE = (250, 50)

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
        self.settings_ = SETTINGS


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
            initialdir=SETTINGS_FOLDER,
            title="Select file",
            filetypes=(("json files", "*.json"),)
        )
        if file_path:
            with open(file_path, "r") as f1, open(SETTINGS_FOLDER + "current.json", "w") as f2:
                self.settings_ = json.load(f1)
                json.dump(self.settings_, f2)
        EventsQ.add(Event.LOAD_BINDS, binds=self.settings_)


    def save_controls(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(
            initialdir=SETTINGS_FOLDER,
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
        with open(SETTINGS_FOLDER + "current.json", "w") as file:
            json.dump(self.settings_, file)
        EventsQ.add(Event.LOAD_BINDS, binds=self.settings_)