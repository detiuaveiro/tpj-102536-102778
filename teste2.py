import pygame
from utils import Subject, Event
from Menu import Menu


class Teste(Subject):

    def __init__(self):
        super().__init__()
        self.fps = 90
        self.set_display_size(1000, 800)
        self.menu = Menu(self)
        self.register_events(
            Event.KEY_DOWN,
            Event.NEW_LEVEL
        )
        self.paused = True
        self.level = 1


    def on_new_frame(self):
        self.keys = []


    def on_key_down(self, key):
        print(key)


    def on_new_level(self, level):
        self.level = level


    def draw(self):
        self.display.fill("white")
        text = pygame.font.SysFont(None, 50).render("Hello World", True, "black")
        text_rect = text.get_rect(center=(500, 400))
        self.display.blit(text, text_rect)
        level_text = pygame.font.SysFont(None, 50).render(f"Level: {self.level}", True, "black")
        level_text_rect = level_text.get_rect(center=(500, 500))
        self.display.blit(level_text, level_text_rect)
        self.menu.draw(self.display)
        

    
if __name__ == "__main__":
    teste = Teste()
    teste.run()