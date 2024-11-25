import pygame
from pygame.sprite import Sprite
from utils import Entity, Subject, Event

class MenuSprite(Sprite):
    
    def __init__(self):
        super().__init__()
        self.active: bool = False
        self.image = pygame.Surface((800, 600))
        self.image.fill("red")
        self.rect = self.image.get_rect()

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)


class Menu(Entity):

    def __init__(self):
        super().__init__()
        self.sprite = MenuSprite()

        self.register_events(
            Event.KEY_DOWN,
        )


    def on_key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.sprite.active = not self.sprite.active


class Teste(Subject):

    def __init__(self):
        super().__init__()
        self.fps = 10
        self.set_display_size(800, 600)
        self.register_events(
            Event.NEW_FRAME,
            Event.KEY_PRESSED,
        )
        self.keys = []
        self.menu = Menu()


    def on_new_frame(self):
        self.keys = []


    def on_key_pressed(self, key):
        print(f"Key pressed: {key}")
        self.keys.append(key)


    def draw(self):
        self.display.fill("white")
        text = pygame.font.SysFont(None, 30).render(str(self.keys), True, "black")
        self.display.blit(text, (10, 10))
        self.menu.sprite.draw(self.display)
        

    
if __name__ == "__main__":
    teste = Teste()
    teste.run()