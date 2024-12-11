from typing import Generator

from utils import Event

class EventsQ:
    """
    Singleton class that manages the events queue and the observers.

    Static Attributes
    -----------------
    _events (list[(Event, dict)]): 
        List of events to be processed.
    _observers (dict[Event, list[callable]]):
        Dictionary of callbacks from observers for each event.
    _observers_paused (dict[Event, list[callable]]):
        Dictionary of callbacks from observers for each event when the game is paused.
    """
    
    _events: list[(Event, dict)] = []
    _observers: dict[Event, list[callable]] = {}
    _observers_paused: dict[Event, list[callable]] = {}


    def __new__(cls) -> None:
        raise Exception("This class is a singleton.")


    @staticmethod
    def add(event: Event, **kwargs) -> None:
        """
        Add an event to the queue.

        Parameters
        ----------
        event (Event):
            Event to be added to the queue.
        kwargs (dict):
            Arguments for the event.
        """
        if event:
            EventsQ._events.append((event, kwargs))


    @staticmethod
    def get() -> Generator[tuple[Event, dict], None, None]:
        """
        Get the events from the queue.

        Yields
        ------
        tuple[Event, dict]:
            Event and arguments.
        """
        while EventsQ._events:
            yield EventsQ._events.pop(0)


    @staticmethod
    def register(event: Event, callback: callable) -> None:
        """
        Register a callback from an observer for an event.

        Parameters
        ----------
        event (Event):
            Event to be observed.
        callback (callable):
            Callback function to be called when the event is triggered.
        """
        if event not in EventsQ._observers:
            EventsQ._observers[event] = []
        EventsQ._observers[event].append(callback)


    @staticmethod
    def register_paused(event: Event, callback: callable) -> None:
        """
        Register a callback from an observer for an event when the game is paused.

        Parameters
        ----------
        event (Event):
            Event to be observed.
        callback (callable):
            Callback function to be called when the event is triggered.
        """
        if event not in EventsQ._observers_paused:
            EventsQ._observers_paused[event] = []
        EventsQ._observers_paused[event].append(callback)


    @staticmethod
    def notify(event: Event, **kwargs) -> None:
        """
        Notify all observers of an event.

        Parameters
        ----------
        event (Event):
            Event to be triggered.
        kwargs (dict):
            Arguments for the event.
        """
        for callback in EventsQ._observers.get(event, []):
            callback(**kwargs)


    @staticmethod
    def notify_paused(event: Event, **kwargs) -> None:
        """
        Notify all observers of an event when the game is paused.

        Parameters
        ----------
        event (Event):
            Event to be triggered.
        kwargs (dict):
            Arguments for the event.
        """
        for callback in EventsQ._observers_paused.get(event, []):
            callback(**kwargs)