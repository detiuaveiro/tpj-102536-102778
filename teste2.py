
from Utils import Subject, Event

class Teste(Subject):
    def __init__(self):
        super().__init__()
        self.fps = 1
        self.register_many(
            Event.UPDATE_GAME,
        )

    def on_update_game(self):
        print("on_update_game")


if __name__ == "__main__":
    t = Teste()
    t.run()