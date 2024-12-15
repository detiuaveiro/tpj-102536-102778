import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def get_rect(self):
        return self.rect
    
    
    def get_blocks(self):
        return [self.rect]