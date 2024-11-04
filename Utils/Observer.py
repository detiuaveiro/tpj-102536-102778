from Utils import Event, Events

class Observer():

    def register(self, *events: Event) -> None:
        for event in events:
            fn = getattr(self, f"on_{event.name.lower()}")
            Events.register(event, fn)