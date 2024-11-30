import pygame
from utils import Entity


class MechanismSprite(pygame.sprite.Sprite):
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Mechanism(Entity):
    def __init__(self):
        super().__init__()
        self.active = False
        self.triggers_group = pygame.sprite.Group()
        self.barriers_group = pygame.sprite.Group()

    
    def add_trigger(self, image, x, y):
        trigger = MechanismSprite("trigger", image, x, y)
        self.triggers_group.add(trigger)

    
    def add_barrier(self, image, x, y):
        barrier = MechanismSprite("barrier", image, x, y)
        self.barriers_group.add(barrier)

    
    def deactivate(self):
        self.active = False
        for sprite in self.triggers_group:
            sprite.deactivate_trigger()

    
    def activate(self):
        self.active = True
        for sprite in self.triggers_group:
            sprite.activate_trigger(True)

    
    def get_trigger_rects(self):
        return [sprite.hitbox_rect for sprite in self.triggers_group]
    

    def get_barrier_rects(self):
        if not self.active:
            return [sprite.hitbox_rect for sprite in self.barriers_group]
        return []
    

    def draw(self, screen):
        self.triggers_group.draw(screen)

        if not self.active:
            self.barriers_group.draw(screen)