
from Utils import Event, Events, Observer, Entity


class E(Entity):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    e = E()
    print(e)