import pygame
from enum import Enum, auto

from utils import Entity, Event, FSM, EventsQ
from sprites import Character as CharacterSprite
from game.consts import SETTINGS, DEATH_FRAMES

TILESIZE = 32
ANIMATION_COOLDOWN = 100
GRAVITY = 0.4
HORIZONTAL_SPEED = 1
VERTICAL_SPEED = 10
PLAYERS = ['Pink Monster', 'Blue Monster']


class Transition(Enum):
    JUMP = auto()
    MOVE = auto()
    ON_GROUND = auto()
    DEFAULT = auto()
    DIE = auto()
    USE = auto()


class States(Enum):
    IDLE = 'idle'
    JUMPING = 'jumping'
    DEATH = 'death'
    RUNNING = 'running'
    USING = 'using'


class Character(Entity):

    def __init__(self, num, x, y, scale):
        super().__init__()
        self.time = pygame.time.get_ticks()
        self.num = num
        self.scale = scale
        self.sprite = CharacterSprite(PLAYERS[num-1], scale)
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 0
        self.on_portal = False
        self.running = False
        self.frames_after_death = 0

        self.register_events(
            Event.KEY_PRESSED,
            Event.UPDATE_GAME,
            Event.DEATH,
            Event.RESET
        )
        self.register_paused_events(
            Event.LOAD_BINDS,
            Event.RESET
        )

        self.setup_binds()
        self.setup_fsm()
        self.setup_sprite(x, y)


    def setup_binds(self, settings=SETTINGS):
        self.binds = settings[self.num-1]
        self.key_mapping = {
            self.binds['right']: (Transition.MOVE, self.right),
            self.binds['left']: (Transition.MOVE, self.left),
            self.binds['jump']: (Transition.JUMP, self.jump),
            self.binds['sprint']: (Transition.MOVE, self.run),
            self.binds['use']: (Transition.USE, self.use)
        }

    
    def setup_fsm(self):
        self.fsm = FSM(States.IDLE)
        self.fsm.set_transitions(
            (Transition.JUMP, States.IDLE, States.JUMPING, self.move),
            (Transition.JUMP, States.RUNNING, States.JUMPING, self.move),
            (Transition.MOVE, States.IDLE, States.RUNNING, self.move),
            (Transition.MOVE, States.RUNNING, States.RUNNING, self.move),
            (Transition.MOVE, States.JUMPING, States.JUMPING, self.move),
            (Transition.ON_GROUND, States.JUMPING, States.IDLE, None),
            (Transition.DEFAULT, States.RUNNING, States.IDLE, None),
            (Transition.DEFAULT, States.IDLE, States.IDLE, None),
            (Transition.DEFAULT, States.JUMPING, States.JUMPING, None),
            (Transition.DIE, States.IDLE, States.DEATH, None),
            (Transition.DIE, States.RUNNING, States.DEATH, None),
            (Transition.DIE, States.JUMPING, States.DEATH, None),
            (Transition.USE, States.IDLE, States.USING, self.move),
            (Transition.DEFAULT, States.USING, States.IDLE, None)
        )


    def on_paused_load_binds(self, binds):
        self.setup_binds(binds)


    def setup_sprite(self, x, y):
        current_state = self.fsm.get_state_str()
        self.sprite.setup_sprite(x, y, current_state, self.direction)


    def run(self):
        self.running = True


    def move(self, key):
        if key not in self.key_mapping:
            return
        _, action = self.key_mapping[key]
        action()


    def use(self):
        EventsQ.add(Event.USE, player=self.num)

    
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

        if self.fsm.get_state() == States.DEATH:
            self.frames_after_death += 1
            if self.frames_after_death == DEATH_FRAMES:
                self.fsm.update(Transition.DEFAULT)
                EventsQ.add(Event.RESTART_LEVEL)

    
    def on_death(self, player):
        if player == self.num:
            self.fsm.update(Transition.DIE)

    
    def on_reset(self, player, x, y):
        if self.num == player:
            self.sprite = CharacterSprite(PLAYERS[self.num-1], self.scale)
            self.setup_fsm()
            self.setup_sprite(x, y)
            self.direction = 0
            self.vel_x = 0
            self.vel_y = 0
            self.running = False
            self.frames_after_death = 0


    def on_paused_reset(self, player, x, y):
        self.on_reset(player, x, y)


    def get_hitbox_rect(self):
        return self.sprite.hitbox_rect
    

    def get_vel(self):
        return self.vel_x, self.vel_y
    

    def draw(self, screen: pygame.Surface):
        self.sprite.draw(screen)