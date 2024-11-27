import pygame
from pathlib import Path
from utils import Entity, Event
from enum import Enum, auto
from .CharacterSprite import CharacterSprite

TILESIZE = 32
ANIMATION_COOLDOWN = 100
GRAVITY = 0.4
HORIZONTAL_SPEED = 1
VERTICAL_SPEED = 10


class Transition(Enum):
    JUMP = auto()
    MOVE = auto()
    ON_GROUND = auto()
    DEFAULT = auto()


class States(Enum):
    IDLE = 'idle'
    JUMPING = 'jumping'
    DEATH = 'death'
    RUNNING = 'running'


class Character(Entity):

    def __init__(self, name, x, y, scale):
        super().__init__()
        self.time = pygame.time.get_ticks()
        self.name = name
        self.scale = scale
        self.sprite = CharacterSprite(name, scale)
        self.key_mapping = {}
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 0
        self.running = False

        self.register_events(
            Event.KEY_PRESSED,
            Event.UPDATE_GAME
        )

        self.init_fsm()
        self.setup_sprite(x, y)

    
    def init_fsm(self):
        self.fsm.set_state(States.IDLE)
        self.fsm.set_transitions(
            (Transition.JUMP, States.IDLE, States.JUMPING, self.move),
            (Transition.JUMP, States.RUNNING, States.JUMPING, self.move),
            (Transition.MOVE, States.IDLE, States.RUNNING, self.move),
            (Transition.MOVE, States.RUNNING, States.RUNNING, self.move),
            (Transition.MOVE, States.JUMPING, States.JUMPING, self.move),
            (Transition.ON_GROUND, States.JUMPING, States.IDLE, None),
            (Transition.DEFAULT, States.RUNNING, States.IDLE, None),
            (Transition.DEFAULT, States.IDLE, States.IDLE, None),
            (Transition.DEFAULT, States.JUMPING, States.JUMPING, None)
        )


    def setup_sprite(self, x, y):
        current_state = self.fsm.get_state_str()
        self.sprite.setup_sprite(x, y, current_state, self.direction)


    def register_keys(self, right, left, jump, run):
        self.key_mapping = {
            right: (Transition.MOVE, self.right),
            left: (Transition.MOVE, self.left),
            jump: (Transition.JUMP, self.jump),
            run: (Transition.MOVE, self.run)
        }


    def run(self):
        self.running = True


    def move(self, key):
        if key not in self.key_mapping:
            return
        _, action = self.key_mapping[key]
        action()

    
    def right(self):
        self.direction = 0
        self.vel_x = HORIZONTAL_SPEED * self.scale

    
    def left(self):
        self.direction = 1
        self.vel_x = -HORIZONTAL_SPEED * self.scale


    def jump(self):
        self.vel_y = -VERTICAL_SPEED


    def on_key_pressed(self, key):
        if key not in self.key_mapping:
            return
        transition, _ = self.key_mapping[key]
        self.fsm.update(transition, key=key)


    def move_x(self):
        if self.running:
            self.vel_x *= 2
        self.sprite.rect.x += self.vel_x
        self.sprite.hitbox_rect.x += self.vel_x


    def move_y(self):
        self.sprite.rect.y += self.vel_y
        self.sprite.hitbox_rect.y += self.vel_y

    
    def collide_x(self, rect):        
        if self.vel_x > 0:
            self.sprite.hitbox_rect.right = rect.left
        else:
            self.sprite.hitbox_rect.left = rect.right
        self.sprite.rect.centerx = self.sprite.hitbox_rect.centerx


    def collide_y(self, rect):
        if self.vel_y < 0:
            self.sprite.hitbox_rect.top = rect.bottom
        else:
            self.sprite.hitbox_rect.bottom = rect.top
            self.fsm.update(Transition.ON_GROUND)
        self.sprite.rect.bottom = self.sprite.hitbox_rect.bottom
        self.vel_y = 0


    def update_sprite(self):
        current_time = pygame.time.get_ticks()
        current_state = self.fsm.get_state_str()
        if current_time - self.time > ANIMATION_COOLDOWN:
            self.time = current_time
            self.sprite.update_image(current_state, self.direction)


    def on_update_game(self):
        self.update_sprite()
        if self.vel_y > GRAVITY:
            self.fsm.update(Transition.JUMP, key=None)
        else:
            self.fsm.update(Transition.DEFAULT)
        self.vel_y += GRAVITY
        self.vel_x = 0
        self.running = False


    def get_hitbox_rect(self):
        return self.sprite.hitbox_rect
    

    def draw(self, screen: pygame.Surface):
        self.sprite.draw(screen)