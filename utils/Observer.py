from utils import Event, EventsQ

class Observer():

    def register_events(self, *events: Event) -> None:
        for event in events:
            fn = getattr(self, f"on_{event.name.lower()}")
            EventsQ.register(event, fn)