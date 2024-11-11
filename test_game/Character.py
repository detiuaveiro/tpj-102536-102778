# Python
import pygame
from pathlib import Path
from common import Directions, States

TILESIZE = 32
ANIMATION_COOLDOWN = 100
GRAVITY = 0.75
HORIZONTAL_SPEED = 1
VERTICAL_SPEED = 12

class Character(pygame.sprite.Sprite):

    def __init__(self, name, x, y, scale):
        super().__init__()
        self.image = None
        self.rect = None
        self.hitbox_rect = None

        # General
        self.name = name
        self.scale = scale

        # Physics
        self.vel_x = 0
        self.vel_y = 0
                
        # Animation
        self.spritesheet = Path(f'assets/{self.name.replace(' ', '')}')
        self.frames = {}
        self.frame_idx = 0
        self.time = pygame.time.get_ticks()
        self.state = States.IDLE
        self.direction = Directions.RIGHT

        self.load_sprites()
        self.initialize_image_and_rect(x, y)


    def load_sprites(self):
        files = [f for f in self.spritesheet.iterdir() if f.is_file() and not f.name.startswith('.')]
        for f in files:
            aux = f.name.split('_')
            state = aux[0].lower()
            n_sprites = int(aux[-1].split('.')[0])
            spritesheet = pygame.image.load(f)
            self.frames[state] = []
            for i in range(n_sprites):
                original = pygame.Surface.subsurface(spritesheet, (i * TILESIZE, 0, TILESIZE, TILESIZE))
                scaled = pygame.transform.scale(original, (TILESIZE * self.scale, TILESIZE * self.scale))
                self.frames[state].append(scaled)

        # To remove until clever solution:
        self.frames['idle'] = self.frames['idle'][:1]


    def initialize_image_and_rect(self, x, y):
        self.image = self.frames[self.state.value][self.frame_idx]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hitbox_rect = self.image.get_bounding_rect()
        self.hitbox_rect.centerx = self.rect.centerx
        self.hitbox_rect.bottom = self.rect.bottom


    def key_pressed(self, key):
        if key == pygame.K_RIGHT:
            self.vel_x = HORIZONTAL_SPEED * self.scale
            self.direction = Directions.RIGHT

        elif key == pygame.K_LEFT:
            self.vel_x = -HORIZONTAL_SPEED * self.scale
            self.direction = Directions.LEFT

        elif key == pygame.K_SPACE and self.vel_y == 0:
            self.jump()


    def key_released(self, key):
        if key in (pygame.K_RIGHT, pygame.K_LEFT):
            self.vel_x = 0

    
    def jump(self):
        self.vel_y = -VERTICAL_SPEED


    def move_x(self):
        self.rect.x += self.vel_x
        self.hitbox_rect.x += self.vel_x


    def move_y(self):
        self.vel_y += GRAVITY
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
        self.rect.bottom = self.hitbox_rect.bottom
        self.vel_y = 0


    def update(self):
        self.update_state()
        self.update_animation()


    def update_state(self):
        if self.vel_y != 0:
            self.state = States.JUMP
        elif self.vel_x != 0:
            self.state = States.RUN
        else:
            self.state = States.IDLE


    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time > ANIMATION_COOLDOWN:
            self.time = current_time
            self.frame_idx = (self.frame_idx + 1) % len(self.frames[self.state.value])
            self.update_image()


    def update_image(self):
        if self.direction == Directions.LEFT:
            self.image = pygame.transform.flip(self.frames[self.state.value][self.frame_idx], 1, 0)
        else:
            self.image = self.frames[self.state.value][self.frame_idx]
        

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    
    def get_hitbox_rect(self):
        return self.hitbox_rect


    def get_pos(self):
        return (
            self.hitbox_rect.x,
            self.hitbox_rect.y,
            self.hitbox_rect.right - self.hitbox_rect.left,
            self.hitbox_rect.bottom - self.hitbox_rect.top,
            self.vel_x,
            self.vel_y
        )
