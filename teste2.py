import pygame

from utils import Subject, Event
# from entities import Menu

class Teste(Subject):

    def __init__(self):
        super().__init__()
        self.fps = 90
        self.set_display_size(1000, 800)
        # self.menu = Menu(self)
        self.register_events(
            Event.KEY_DOWN,
        )
        self.paused = False
        self.surface = pygame.Surface((900, 700))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (500, 350)


    def on_key_down(self, key):
        if key == pygame.K_LEFT:
            self.surface_rect.move_ip(-50, 0)
        elif key == pygame.K_RIGHT:
            self.surface_rect.move_ip(50, 0)
        elif key == pygame.K_UP:
            self.surface_rect.move_ip(0, 50)
        elif key == pygame.K_DOWN:
            self.surface_rect.move_ip(0, -50)
        print(self.surface_rect.center)


    def draw_box(self, surface):
        pygame.draw.rect(surface, "black", (100, 100, 200, 200))


    def draw(self):
        self.display.fill("white")
        self.surface.fill("blue")
        self.draw_box(self.surface)
        self.display.blit(self.surface, self.surface_rect)
        # self.menu.draw(self.display)

        

    
if __name__ == "__main__":
    teste = Teste()
    teste.run()