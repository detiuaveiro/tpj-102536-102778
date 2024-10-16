import pygame
from pygame import Surface
from pygame.sprite import Group
from pygame.time import Clock
import logging
import json
from typing import Generator

from Utils import Event, Observer, Events

class Subject(Observer):

    def __init__(self):
        Observer.__init__(self)
        pygame.init()
        self.fps: int = 60
        self.display_size: tuple[int, int] = (800, 600)
        self.running: bool = True
        self.sprites: Group = Group()
        self.display: Surface = None
        self.clock: Clock = Clock()

        self.frame = 0
        logging.basicConfig(
            filename="game.log",
            format='%(message)s',
            level=logging.DEBUG,
            filemode='w'
        )


    def process_input(self) -> None:
        pressed_keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                Events.add(Event.KEY_PRESSED, key=event.key)
                pressed_keys.append(event.key)
        logging.info(json.dumps({
            "frame": self.frame,
            "event": "KEY_PRESSED",
            "keys": pressed_keys
        }))
        self.frame += 1


    def update_game(self) -> None:
        for event, kwargs in Events.get():
            Events.notify(event, **kwargs)


    def render(self) -> None:
        self.display.fill("white")
        self.sprites.update()
        self.sprites.draw(self.display)
        pygame.display.flip()
        self.clock.tick(self.fps)


    def replay(self, file) -> Generator:
        with open(file, "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            data = json.loads(line)
            if data["event"] == "KEY_PRESSED":
                for key in data["keys"]:
                    Events.add(Event.KEY_PRESSED, key=key)
                logging.info(json.dumps({
                    "frame": i,
                    "event": "KEY_PRESSED",
                    "keys": data["keys"]
                }))
            if i == len(lines) - 1:
                self.running = False
            yield
            

    def run(self, file=None) -> None:
        self.display = pygame.display.set_mode(self.display_size)
        if file:
            replay = self.replay(file)
        while self.running:
            if file:
                next(replay)
            else:
                self.process_input()
            Events.add(Event.UPDATE_GAME)
            self.update_game()
            self.render()
        pygame.quit()
        logging.shutdown()