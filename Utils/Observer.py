from Utils import Event, Events

class Observer():

    def __init__(self): 
        self.callbacks: dict[Event, callable] = {}
    

    def on_notify(self, event: Event, **kwargs) -> None:
        if kwargs:
            self.callbacks.get(event, lambda: None)(**kwargs)
        else:
            self.callbacks.get(event, lambda: None)()


    def register(self, event: Event, callback: callable) -> None:
        self.callbacks[event] = callback
        Events.register(event, self)


    def unregister(self, event: Event) -> None:
        Events.unregister(event, self)
        self.callbacks.pop(event)