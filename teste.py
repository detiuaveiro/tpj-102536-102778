from Utils import Subject, Event

class Test(Subject):

    def __init__(self):
        super().__init__()
        self.fps = 1
        self.register(Event.KEY_PRESSED, self.print_key)
        self.register(Event.UPDATE_GAME, self.update)


    def print_key(self, key: int):
        print(f"Key: {key}")

    def update(self):
        print("update")
    

a = Test()
a.run()