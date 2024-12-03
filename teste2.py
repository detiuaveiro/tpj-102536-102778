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
        self.fps = 90
        self.set_display_size(1000, 800)
        self.menu = Menu(self)
        self.register_events(
            Event.KEY_DOWN,
        )
        self.paused = True
        self.surface = pygame.Surface((900, 1500))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (500, 750)
        self.display_rect = self.display.get_rect()
        self.point = Point(500, 350)
        self.offset = 0



    def on_key_down(self, key):
        if key == pygame.K_DOWN:
            self.point.move_down(20)
            self.offset += 20
            if self.offset > 250:
                self.surface_rect.y -= 20
                self.offset -= 20
        elif key == pygame.K_UP:
            self.point.move_up(20)
            self.offset -= 20
            if self.offset < -150:
                self.surface_rect.y += 20
                self.offset += 20
        print(self.offset)



    def draw_box(self, surface):
        pygame.draw.rect(surface, "black", (100, 100, 200, 200))


    def draw(self):
        self.display.fill("white")
        self.surface.fill("blue")
        self.draw_box(self.surface)
        self.point.draw(self.surface)
        self.display.blit(self.surface, self.surface_rect)
        pygame.draw.line(self.display, "green", (0, 200), (1000, 200))
        pygame.draw.line(self.display, "green", (0, 600), (1000, 600))
        self.menu.draw(self.display)

        

    
if __name__ == "__main__":
    teste = Teste()
    teste.run()