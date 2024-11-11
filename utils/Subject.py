import pygame
from pygame import Surface
from pygame.time import Clock
import logging
import json
from abc import ABC, abstractmethod

from utils import Event, Observer, EventsQ

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
        self.keys_down: set[int] = set()

        logging.basicConfig(
            filename="game.log",
            format='%(message)s',
            level=logging.DEBUG,
            filemode='w'
        )


    @abstractmethod
    def render(self) -> None:
        pass


    def set_display_size(self, width: int, height: int) -> None:
        self.display = pygame.display.set_mode((width, height))


    def process_input(self) -> None:
        EventsQ.add(Event.NEW_FRAME)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (event.type == pygame.KEYDOWN):
                self.keys_down.add(event.key)
            elif (event.type == pygame.KEYUP):
                self.keys_down.remove(event.key)

        if pressed_keys := list(self.keys_down):
            self.log(Event.KEY_PRESSED, keys=pressed_keys)
            for key in pressed_keys:
                EventsQ.add(Event.KEY_PRESSED, key=key)
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
        EventsQ.add(Event.UPDATE_GAME)
        for event, kwargs in EventsQ.get():
            EventsQ.notify(event, **kwargs)


    def render_(self) -> None:
        self.render()
        pygame.display.flip()
        self.clock.tick(self.fps)


    def run(self) -> None:
        while self.running:
            self.process_input()
            self.update_game()
            self.render_()
        pygame.quit()
        logging.shutdown()