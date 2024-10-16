import pygame
from pygame import Surface
from pygame.sprite import Sprite

from Utils import Event, Observer
from SnakeGame.Direction import Direction

class Snake(Observer, Sprite):

    def __init__(self, color, width, height, scale):
        Observer.__init__(self)
        Sprite.__init__(self)
        self.color = color
        self.width = width
        self.height = height
        self.scale = scale
        self.body = [
            (40, 20),
            (39, 20),
            (38, 20),
        ]
        self.direction = Direction.RIGHT
        self.new_direction = Direction.RIGHT

        self.image = Surface((self.width * self.scale, self.height * self.scale), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.update()

        self.key_map = {
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT
        }

        self.register_many(
            Event.KEY_PRESSED,
            Event.UPDATE_GAME,
            Event.EAT
        )


    def on_key_pressed(self, key: int):
        if key in self.key_map:
            self.new_direction = self.key_map[key]

    
    def on_update_game(self):
        if self.new_direction.is_inverted(self.direction):
            self.new_direction = self.direction
        new_head = (self.body[0][0] + self.new_direction.value[0], self.body[0][1] + self.new_direction.value[1])
        self.body = [new_head] + self.body[:-1]
        self.direction = self.new_direction


    def on_eat(self):
        tail = self.body[-1]
        self.body.append(tail)


    def update(self):
        self.image.fill((0, 0, 0, 0))
        for x, y in self.body:
            pygame.draw.rect(self.image, self.color, (x * self.scale, y * self.scale, self.scale, self.scale))


    def self_collision(self):
        return self.body[0] in self.body[1:]