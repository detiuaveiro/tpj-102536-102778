from typing import Generator

from utils import Event

class EventsQ:
    
    _events: list[(Event, dict)] = []
    _observers: dict[Event, list[callable]] = {}


    @staticmethod
    def add(event: Event, **kwargs) -> None:
        if event:
            EventsQ._events.append((event, kwargs))


    @staticmethod
    def get() -> Generator[tuple[Event, dict], None, None]:
        while EventsQ._events:
            yield EventsQ._events.pop(0)


    @staticmethod
    def register(event: Event, callback: callable) -> None:
        if event not in EventsQ._observers:
            EventsQ._observers[event] = []
        EventsQ._observers[event].append(callback)


    @staticmethod
    def notify(event: Event, **kwargs) -> None:
        for callback in EventsQ._observers.get(event, []):
            callback(**kwargs)


    @staticmethod
    def notify_one(event: Event, obj: object, **kwargs) -> None:
        for callback in EventsQ._observers.get(event, []):
            if callback.__self__ == obj:
                callback(**kwargs)