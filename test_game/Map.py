import pygame
import csv
from pathlib import Path
import json


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self, display: pygame.surface.Surface):
        display.blit(self.image, self.rect)


    def get_rect(self):
        return self.rect


class Map:
    def __init__(self, map_folder, scale):
        self.path = Path(map_folder)
        self.scale = scale
        self.tileset_img = None
        self.tileset_cols = None
        self.tileset_rows = None
        self.tile_size = None
        self.tiles = []
        self.map_tiles = pygame.sprite.Group()
        self.map_rects = []
        
        self.load_metadata()
        self.load_tiles()
        self.load_map()


    def load_metadata(self):
        with open(self.path / "map.json", "r") as f:
            map_metadata = json.load(f)
            self.tileset_img = map_metadata['tileset_image']
            self.tileset_cols = map_metadata['tileset_columns']
            self.tileset_rows = map_metadata['tileset_rows']
            self.tile_size = map_metadata['tile_size']


    def load_tiles(self):
        image = pygame.image.load(self.tileset_img)
        for y in range(self.tileset_rows):
            for x in range(self.tileset_cols):
                original = image.subsurface((x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                scaled = pygame.transform.scale(original, (self.tile_size * self.scale, self.tile_size * self.scale))
                self.tiles.append(scaled)


    def load_map(self):
        map_details = self.read_csv()
        
        for y, row in enumerate(map_details):
            for x, tile in enumerate(row):
                tile_idx = int(tile)
                if tile_idx >= 0:
                    tile_obj = Tile(self.tiles[tile_idx], x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                    self.map_tiles.add(tile_obj)
                    self.map_rects.append(tile_obj.get_rect())


    def read_csv(self):
        map_details = []
        with open(self.path / "map.csv") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                map_details.append(row)
        return map_details
    

    def get_rects(self):
        return self.map_rects


    def draw(self, display: pygame.surface.Surface):
        self.map_tiles.draw(display)