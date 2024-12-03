import pygame

from utils import Subject, Event
from entities import Menu

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_down(self, step):
        self.y += step

    def move_up(self, step):
        self.y -= step

    def draw(self, surface):
        pygame.draw.circle(surface, "red", (self.x, self.y), 5)


class Teste(Subject):

    def __init__(self):
        super().__init__()
        self.fps = 5
        self.set_display_size(1000, 800)
        self.display_rect = self.display.get_rect()
        self.menu = Menu(self)
        self.register_events(
            Event.KEY_DOWN,
            Event.UPDATE_GAME,
        )
        self.paused = True
        self.surface = pygame.Surface((900, 1500))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = self.display_rect.center
        
        self.point = Point(450, 800)


    def on_key_down(self, key):
        if key == pygame.K_DOWN:
            self.point.move_down(20)
        elif key == pygame.K_UP:
            self.point.move_up(20)

    
    def on_update_game(self):
        absolute_position = self.point.y + self.surface_rect.y
        if absolute_position > 600:
            self.surface_rect.y -= 30
        elif absolute_position < 200:
            self.surface_rect.y += 30


    def draw_box(self, surface):
        pygame.draw.rect(surface, "black", (100, 300, 200, 200))


    def draw(self):
        self.display.fill("white")
        self.surface.fill("blue")
        pygame.draw.circle(self.surface, "black", (450, 750), 5)
        self.draw_box(self.surface)
        self.point.draw(self.surface)
        self.display.blit(self.surface, self.surface_rect)
        pygame.draw.line(self.display, "green", (0, 200), (1000, 200))
        pygame.draw.line(self.display, "green", (0, 600), (1000, 600))
        self.menu.draw(self.display)

        

    
if __name__ == "__main__":
    teste = Teste()
    teste.run()