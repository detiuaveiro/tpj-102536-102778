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
        self.replay: list[tuple[int, list]] = [] # frame, keys

        logging.basicConfig(
            filename="game.log",
            format='%(message)s',
            level=logging.DEBUG,
            filemode='w'
        )


    @abstractmethod
    def render(self) -> None:
        pass


    @property
    def replaying(self) -> bool:
        return bool(self.replay)


    def set_fps(self, fps: int) -> None:
        self.fps = fps


    def set_display_size(self, width: int, height: int) -> None:
        self.display = pygame.display.set_mode((width, height))


    def set_replay(self, logs: list[dict]) -> None:
        self.frame = 0
        self.replay = [
            (log["frame"], log["keys"])
            for log in logs
            if log["event"] == Event.KEY_PRESSED.name and log.get("keys")
        ]


    def process_input(self) -> None:
        pressed_keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (
                event.type == pygame.KEYDOWN
                or event.type == pygame.K_ESCAPE
                or not self.replaying
                or self.paused
            ):
                Events.add(Event.KEY_PRESSED, key=event.key)
                pressed_keys.append(event.key)

        if self.replaying:
            frame, keys = self.replay[0]
            if frame == self.frame:
                for key in keys:
                    Events.add(Event.KEY_PRESSED, key=key)
                self.replay.pop(0)
            pressed_keys = keys

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