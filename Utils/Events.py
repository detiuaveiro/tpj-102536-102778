from typing import Generator, TYPE_CHECKING

from Utils import Event

if TYPE_CHECKING:
    from Utils import Observer

class Events:
    
    _events: list[(Event, dict)] = []
    _observers: dict[Event, list['Observer']] = {}


    @staticmethod
    def add(event: Event, **kwargs) -> None:
        if event:
            Events._events.append((event, kwargs))


    @staticmethod
    def get() -> Generator[tuple[Event, dict], None, None]:
        while Events._events:
            yield Events._events.pop(0)


    @staticmethod
    def register(event: Event, observer: 'Observer') -> None:
        if event not in Events._observers:
            Events._observers[event] = []
        Events._observers[event].append(observer)

    
    @staticmethod
    def unregister(event: Event, observer: 'Observer') -> None:
        if event in Events._observers:
            Events._observers[event].remove(observer)


    @staticmethod
    def notify(event: Event, **kwargs) -> None:
        event_handlers = Events._observers.get(event, [])
        for observer in event_handlers:
            observer.on_notify(event, **kwargs)
