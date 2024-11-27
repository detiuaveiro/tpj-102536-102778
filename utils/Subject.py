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

        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()


    @abstractmethod
    def draw(self) -> None:
        pass


    def set_display_size(self, width: int, height: int) -> None:
        self.display = pygame.display.set_mode((width, height))


    def process_input(self) -> None:
        EventsQ.add(Event.NEW_FRAME)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (event.type == pygame.KEYDOWN):
                EventsQ.add(Event.KEY_DOWN, key=event.key)
                self.keys_down.add(event.key)
            elif (event.type == pygame.KEYUP):
                EventsQ.add(Event.KEY_UP, key=event.key)
                self.keys_down.remove(event.key)
                
        all_keys = list(self.keys_down) + self.process_joysticks()
        if all_keys:
            self.log(Event.KEY_PRESSED, keys=all_keys)
            for key in all_keys:
                EventsQ.add(Event.KEY_PRESSED, key=key)
        self.frame += 1


    def process_joysticks(self) -> list[str]:
        keys = []
        for id, joystick in enumerate(self.joysticks):
            for i in range(joystick.get_numbuttons()):
                if joystick.get_button(i) == 1:
                    keys.append(f"js_{id}_b_{i}")
            for i in range(joystick.get_numhats()):
                hat = joystick.get_hat(i)
                if hat[0] != 0:
                    keys.append(f"js_{id}_h_{i}_x_{hat[0]}")
                if hat[1] != 0:
                    keys.append(f"js_{id}_h_{i}_y_{hat[1]}")
            for i in range(joystick.get_numaxes()):
                val = joystick.get_axis(i)
                if i in (4, 5):
                    if val > 0:
                        keys.append(f"js_{id}_t_{i}_1")
                elif val > 0.3:
                    keys.append(f"js_{id}_a_{i}_1")
                elif val < -0.3:
                    keys.append(f"js_{id}_a_{i}_-1")
        return keys


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
            if self.paused:
                EventsQ.notify_paused(event, **kwargs)
            else:
                EventsQ.notify(event, **kwargs)
                

    def render(self) -> None:
        self.draw()
        pygame.display.flip()
        self.clock.tick(self.fps)


    def run(self) -> None:
        while self.running:
            self.process_input()
            self.update_game()
            self.render()
        print("Exiting game")
        pygame.quit()
        logging.shutdown()