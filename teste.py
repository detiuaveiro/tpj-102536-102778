from Utils import Subject, Event

class Test(Subject):

    def __init__(self):
        super().__init__()
        self.fps = 1
        self.register_many(
            Event.KEY_PRESSED, 
            Event.UPDATE_GAME
        )

    def on_key_pressed(self, key: int):
        print(f"Key: {key}")

    def on_update_game(self):
        print("update")
    

a = Test()
# a.run()
a.run("replay.jsonl")

# print(Event.KEY_PRESSED.name)