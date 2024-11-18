import pygame
from pathlib import Path
from utils import Entity, Event
from Game.States import States

TILESIZE = 32
ANIMATION_COOLDOWN = 100
GRAVITY = 0.75
HORIZONTAL_SPEED = 1
VERTICAL_SPEED = 12


class Character(Entity):

    def __init__(self, name, x, y, scale):
        super().__init__()
        self.time = pygame.time.get_ticks()
        self.name = name
        self.scale = scale
        self.key_mapping = {}
        self.frames = {} # {state: [[right], [left]]}
        self.frame_idx = 0
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 0 # 0: right, 1: left
        
        self.fsm.set_transitions(
            (Event.JUMP, States.IDLE, States.JUMPING, self.jump),
            (Event.JUMP, States.RUNNING, States.JUMPING, self.jump),
            (Event.MOVE_RIGHT, States.IDLE, States.RUNNING, self.right),
            (Event.MOVE_RIGHT, States.RUNNING, States.RUNNING, self.right),
            (Event.MOVE_RIGHT, States.JUMPING, States.JUMPING, self.right),
            (Event.MOVE_LEFT, States.IDLE, States.RUNNING, self.left),
            (Event.MOVE_LEFT, States.RUNNING, States.RUNNING, self.left),
            (Event.MOVE_LEFT, States.JUMPING, States.JUMPING, self.left),
            (Event.ON_GROUND, States.JUMPING, States.IDLE, None),
            (Event.NONE, States.RUNNING, States.IDLE, None),
            (Event.NONE, States.IDLE, States.IDLE, None),
            (Event.NONE, States.JUMPING, States.JUMPING, None)
        )
        self.fsm.set_state(States.IDLE)

        self.register_events(
            Event.KEY_PRESSED,
            Event.UPDATE_GAME
        )

        self.load_sprites()
        self.initialize_image_and_rect(x, y)


    def load_sprites(self):
        spritesheet = Path(f'Game/assets/{self.name.replace(' ', '')}')
        files = [f for f in spritesheet.iterdir() if f.is_file() and not f.name.startswith('.')]
        for f in files:
            aux = f.name.split('_')
            state = aux[0].lower()
            n_sprites = int(aux[-1].split('.')[0])
            spritesheet = pygame.image.load(f)
            self.frames[state] = [[], []]
            for i in range(n_sprites):
                original = pygame.Surface.subsurface(spritesheet, (i * TILESIZE, 0, TILESIZE, TILESIZE))
                scaled = pygame.transform.scale(original, (TILESIZE * self.scale, TILESIZE * self.scale))
                flipped = pygame.transform.flip(scaled, 1, 0)
                self.frames[state][0].append(scaled)
                self.frames[state][1].append(flipped)


    def initialize_image_and_rect(self, x, y):
        current_state = self.fsm.get_state_str()
        self.image = self.frames[current_state][self.direction][self.frame_idx]
        self.rect = self.image.get_rect()
        self.hitbox_rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox_rect.centerx = self.rect.centerx
        self.hitbox_rect.bottom = self.rect.bottom


    def register_keys(self, right, left, jump):
        self.key_mapping = {
            right: Event.MOVE_RIGHT,
            left: Event.MOVE_LEFT,
            jump: Event.JUMP
        }

    
    def right(self):
        self.direction = 0
        self.vel_x = HORIZONTAL_SPEED * self.scale

    
    def left(self):
        self.direction = 1
        self.vel_x = -HORIZONTAL_SPEED * self.scale

    
    def jump(self):
        self.vel_y = -VERTICAL_SPEED


    def on_key_pressed(self, key):
        if key in self.key_mapping:
            event = self.key_mapping[key]
            self.fsm.update(event)


    def move_x(self):
        self.rect.x += self.vel_x
        self.hitbox_rect.x += self.vel_x


    def move_y(self):
        self.rect.y += self.vel_y
        self.hitbox_rect.y += self.vel_y

    
    def collide_x(self, rect):        
        if self.vel_x > 0:
            self.hitbox_rect.right = rect.left
        else:
            self.hitbox_rect.left = rect.right
        self.rect.centerx = self.hitbox_rect.centerx


    def collide_y(self, rect):
        if self.vel_y < 0:
            self.hitbox_rect.top = rect.bottom
        else:
            self.hitbox_rect.bottom = rect.top
            self.fsm.update(Event.ON_GROUND)
        self.rect.bottom = self.hitbox_rect.bottom
        self.vel_y = 0


    def update_animation(self):
        current_time = pygame.time.get_ticks()
        current_state = self.fsm.get_state_str()
        if current_time - self.time > ANIMATION_COOLDOWN:
            self.time = current_time
            self.frame_idx = (self.frame_idx + 1) % len(self.frames[current_state][self.direction])
            self.image = self.frames[current_state][self.direction][self.frame_idx]
    

    def on_update_game(self):
        print(self.fsm.get_state_str())
        self.update_animation()
        self.fsm.update(Event.NONE)
        self.vel_y += GRAVITY
        self.vel_x = 0


    def get_hitbox_rect(self):
        return self.hitbox_rect
    

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)