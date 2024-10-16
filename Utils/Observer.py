from Utils import Event, Events

class Observer():

    def __init__(self): 
        self.callbacks: dict[Event, callable] = {}
    

    def on_notify(self, event: Event, **kwargs) -> None:
        self.callbacks.get(event, lambda: None)(**kwargs)



    def register(self, event: Event, callback: callable) -> None:
        self.callbacks[event] = callback
        Events.register(event, self)


    def unregister(self, event: Event) -> None:
        Events.unregister(event, self)
        self.callbacks.pop(event)


    def register_many(self, *events: list[Event]) -> None:
        for event in events:
            fn = getattr(self, f"on_{event.name.lower()}")
            self.register(event, fn)