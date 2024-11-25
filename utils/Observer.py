from utils import Event, EventsQ

class Observer():

    def register_events(self, *events: Event) -> None:
        for event in events:
            fn = getattr(self, f"on_{event.name.lower()}")
            EventsQ.register(event, fn)

    def register_paused_events(self, *events: Event) -> None:
        for event in events:
            fn = getattr(self, f"on_paused_{event.name.lower()}")
            EventsQ.register_paused(event, fn)