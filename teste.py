import pygame

from utils import Subject, Event

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


    def on_new_frame(self):
        self.keys = []


    def on_key_pressed(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        print(f"Key pressed: {key}")
        self.keys.append(key)


    def render(self):
        self.display.fill("white")
        text = pygame.font.SysFont(None, 36).render(str(self.keys), True, "black")
        self.display.blit(text, (10, 10))

    
if __name__ == "__main__":
    teste = Teste()
    teste.run()
