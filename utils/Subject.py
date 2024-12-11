import pygame
from pygame import Surface
from pygame.time import Clock
import logging
import json
import tkinter as tk
from abc import ABC, abstractmethod

from utils import Event, Observer, EventsQ

class Subject(Observer, ABC):
    """
    Base class for the game loop and to notify observers of events.
    """

    def __init__(self):
        """
        Attributes
        ----------
        fps (int):
            Frames per second for the game.
        running (bool):
            Flag to keep the game running.
        paused (bool):
            Flag to pause the game.
        display (Surface):
            Display surface for the game.
        clock (Clock):
            Clock to keep track of the game time.
        frame (int):
            Frame number of the game.
        logs (list[dict]):
            List of logs for the game.
        """
        Observer.__init__(self)
        root = tk.Tk()
        root.withdraw()
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
        """
        Abstract method to draw the game.
        """
        pass


    def set_display_size(self, width: int, height: int) -> None:
        """
        Set the display size for the game.

        Parameters
        ----------
        width (int):
            Width of the display.
        height (int):
            Height of the display.
        """
        self.display = pygame.display.set_mode((width, height))


    def process_input(self) -> None:
        """
        Process input events for the game, adding them to the queue.
        """
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
                
        js_keys = self.process_joysticks()
        for key in js_keys:
            EventsQ.add(Event.KEY_DOWN, key=key)
        all_keys = list(self.keys_down) + js_keys
        if all_keys:
            self.log(Event.KEY_PRESSED, keys=all_keys)
            for key in all_keys:
                EventsQ.add(Event.KEY_PRESSED, key=key)
        self.frame += 1


    def process_joysticks(self) -> list[str]:
        """
        Process joystick events for the game.

        Returns
        -------
        list[str]:
            List of keys pressed in the joysticks.
        """
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
        """
        Log an event with its arguments.

        Parameters
        ----------
        event (Event):
            Event to be logged.
        kwargs (dict):
            Arguments for the event.
        """
        msg = json.dumps({
            "frame": self.frame,
            "event": event.name,
            **kwargs
        })
        self.logs.append(msg)
        logging.info(msg)


    def update_game(self) -> None:
        """
        Notify observers of events.
        """
        EventsQ.add(Event.UPDATE_GAME)
        for event, kwargs in EventsQ.get():
            if self.paused:
                EventsQ.notify_paused(event, **kwargs)
            else:
                EventsQ.notify(event, **kwargs)
                

    def render(self) -> None:
        """
        Render the game.
        """
        self.draw()
        pygame.display.flip()
        self.clock.tick(self.fps)


    def run(self) -> None:
        """
        Run the game loop.
        """
        while self.running:
            self.process_input()
            self.update_game()
            self.render()
        print("Exiting game")
        pygame.joystick.quit()
        pygame.quit()
        logging.shutdown()