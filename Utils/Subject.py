import pygame
from pygame import Surface
from pygame.sprite import Group
from pygame.time import Clock
import logging
import json

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
            "keys": pressed_keys
        }))
        self.frame += 1


    def update_game(self) -> None:
        Events.add(Event.UPDATE_GAME)
        for event, kwargs in Events.get():
            Events.notify(event, **kwargs)


    def render(self) -> None:
        self.display.fill("white")
        self.sprites.update()
        self.sprites.draw(self.display)
        pygame.display.flip()
        self.clock.tick(self.fps)


    def run(self) -> None:
        self.display = pygame.display.set_mode(self.display_size)
        while self.running:
            self.process_input()
            self.update_game()
            self.render()
        pygame.quit()
        logging.shutdown()