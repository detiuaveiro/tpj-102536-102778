import pygame
from pathlib import Path
from itertools import cycle

TILESIZE = 32

class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, name, scale):
        super().__init__()
        self.scale = scale
        self.name = name
        self.frames = {}
        self.frames_cycles = {}
        self.frame_idx = 0
        self.state = None
        self.image = None
        self.rect = None
        self.hitbox_rect = None
        self.load_images()

    
    def load_images(self):
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

            # Frame lists to cycles
            right, left = self.frames[state]
            self.frames[state] = [cycle(right), cycle(left)]


    def setup_sprite(self, x, y, state, direction):
        self.state = state
        self.image = next(self.frames[state][direction])
        self.rect = self.image.get_rect()
        self.hitbox_rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox_rect.centerx = self.rect.centerx
        self.hitbox_rect.bottom = self.rect.bottom


    def update_image(self, state, direction):
        self.image = next(self.frames[state][direction])

    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)