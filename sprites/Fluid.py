import pygame


class Fluid(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.hitbox_rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox_rect.centerx = self.rect.centerx
        self.hitbox_rect.bottom = self.rect.bottom


    def draw(self, screen):
        screen.blit(self.image, self.rect)