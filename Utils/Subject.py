import pygame
from pygame import Surface
from pygame.time import Clock
import logging
import json
from abc import ABC, abstractmethod

from Utils import Event, Observer, Events

class Subject(Observer, ABC):

    def __init__(self):
        Observer.__init__(self)
        pygame.init()
        self.fps: int = 60
        self.running: bool = True
        self.paused: bool = False
        self.display: Surface = None
        self.clock: Clock = Clock()

        self.frame: int = 0
        self.logs: list[dict] = []

        logging.basicConfig(
            filename="game.log",
            format='%(message)s',
            level=logging.DEBUG,
            filemode='w'
        )


    @abstractmethod
    def render(self) -> None:
        pass


    def set_fps(self, fps: int) -> None:
        self.fps = fps


    def set_display_size(self, width: int, height: int) -> None:
        self.display = pygame.display.set_mode((width, height))


    def process_input(self) -> None:
        pressed_keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (event.type == pygame.KEYDOWN):
                Events.add(Event.KEY_PRESSED, key=event.key)
                pressed_keys.append(event.key)

        if pressed_keys:
            self.log(Event.KEY_PRESSED, keys=pressed_keys)
        self.frame += 1


    def log(self, event: Event, **kwargs) -> None:
        msg = json.dumps({
            "frame": self.frame,
            "event": event.name,
            **kwargs
        })
        self.logs.append(msg)
        logging.info(msg)


    def update_game(self) -> None:
        Events.add(Event.UPDATE_GAME)
        for event, kwargs in Events.get():
            Events.notify(event, **kwargs)


    def run(self) -> None:
        while self.running:
            self.process_input()
            self.update_game()
            self.render()
        pygame.quit()
        logging.shutdown()