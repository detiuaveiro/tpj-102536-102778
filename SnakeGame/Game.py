
from Utils import Subject, Event, Events

from SnakeGame.Snake import Snake
from SnakeGame.Food import Food

class Game(Subject):

    def __init__(self):
        super().__init__()
        self.scale = 10
        self.width = 80
        self.height= 40
        self.display_size = (self.width * self.scale, self.height * self.scale)
        self.fps = 10
        
        self.snake = Snake((0, 255, 0), self.width, self.height, self.scale)
        self.food = Food((255, 0, 0), self.width, self.height, self.scale)
        self.sprites.add(self.snake)
        self.sprites.add(self.food)

        self.register(
            Event.UPDATE_GAME,
        )

    def on_update_game(self):
        if self.snake.body[0] == self.food.position:
            Events.notify(Event.EAT)
        if self.snake.body[0][0] < 0 or self.snake.body[0][0] >= self.width or self.snake.body[0][1] < 0 or self.snake.body[0][1] >= self.height:
            self.running = False
        if self.snake.self_collision():
            self.running = False