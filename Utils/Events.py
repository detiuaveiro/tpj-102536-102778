from typing import Generator

from Utils import Event

class Events:
    
    _events: list[(Event, dict)] = []
    _observers: dict[Event, list[callable]] = {}


    @staticmethod
    def add(event: Event, **kwargs) -> None:
        if event:
            Events._events.append((event, kwargs))


    @staticmethod
    def get() -> Generator[tuple[Event, dict], None, None]:
        while Events._events:
            yield Events._events.pop(0)


    @staticmethod
    def register(event: Event, callback: callable) -> None:
        if event not in Events._observers:
            Events._observers[event] = []
        Events._observers[event].append(callback)


    @staticmethod
    def notify(event: Event, **kwargs) -> None:
        for callback in Events._observers.get(event, []):
            callback(**kwargs)
