from utils import Event, EventsQ

class Observer():
    """
    Base Observer class to register events and get notified when they are triggered.
    """

    def register_events(self, *events: Event) -> None:
        """
        Register events for the observer.

        Parameters
        ----------
        events (Event):
            Events to be registered
        """
        for event in events:
            fn = getattr(self, f"on_{event.name.lower()}")
            EventsQ.register(event, fn)


    def register_paused_events(self, *events: Event) -> None:
        """
        Register events for the observer when the game is paused.

        Parameters
        ----------
        events (Event):
            Events to be registered
        """
        for event in events:
            fn = getattr(self, f"on_paused_{event.name.lower()}")
            EventsQ.register_paused(event, fn)