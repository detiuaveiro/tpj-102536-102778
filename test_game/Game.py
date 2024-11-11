import pygame
from Map import Map
from Character import Character

DISPLAY_W, DISPLAY_H = 960, 640
SCALE = 2
MAP_FOLDER = "Maps/4"


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))
        self.clock = pygame.time.Clock()
        self.running = True

        # Map
        self.map = Map(MAP_FOLDER, scale=SCALE)
        self.map_rects = self.map.get_rects()

        # Player
        self.player = Character('Pink Monster', x=100, y=200, scale=SCALE)


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.player.key_pressed(event.key)
            elif event.type == pygame.KEYUP:

                self.player.key_released(event.key)


    def draw(self):
        self.screen.fill("black")
        self.map.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)


    def run(self):
        while self.running:
            self.handle_input()

            self.player.move_x()
            self.collisions_x(self.player)
            self.player.move_y()
            self.collisions_y(self.player)
            self.player.update()

            self.draw()
        pygame.quit()


    def collision_rect(self, player):
        hitbox_rect = player.get_hitbox_rect()
        rects_idx = hitbox_rect.collidelistall(self.map_rects)
        if rects_idx:
            return self.map_rects[rects_idx[0]]
        return None
    

    def collisions_x(self, player):
        if rect := self.collision_rect(player):
            player.collide_x(rect)


    def collisions_y(self, player):
        if rect := self.collision_rect(player):
            player.collide_y(rect)