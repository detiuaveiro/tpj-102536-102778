import pygame


class Mechanism(pygame.sprite.Sprite):

    def __init__(self, type, image, x, y):
        super().__init__()
        self.type = type
        self.image = image
        self.rect = self.image.get_rect()
        self.hitbox_rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox_rect.centerx = self.rect.centerx
        self.hitbox_rect.bottom = self.rect.bottom

        self.trigger_images = [
            image,
            pygame.transform.scale(image, (image.get_width(), image.get_height() + 5))
        ]


    def activate_trigger(self, pressed):
        self.image = self.trigger_images[pressed]


    def deactivate_trigger(self):
        self.image = self.trigger_images[0]
