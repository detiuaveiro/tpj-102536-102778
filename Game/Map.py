import pygame
import csv
from pathlib import Path
import json
from .Tile import Tile
from .Fluid import Fluid
from .Mechanism import Mechanism
from utils import Locator


class Map:
    def __init__(self, map_folder, scale):
        self.path = Path(map_folder)
        self.scale = scale
        self.bg_img_path = None
        self.bg_img = None
        self.tileset_img = None
        self.tileset_cols = None
        self.tileset_rows = None
        self.tile_size = None
        self.tiles = []
        self.tile_rects = []
        self.water = Fluid("water")
        self.lava = Fluid("lava")
        self.mechanisms = []
        self.tiles_group = pygame.sprite.Group()

        Locator.add(Fluid, self.water)
        Locator.add(Fluid, self.lava)
        
        self.load_metadata()
        self.load_tiles()
        self.load_map()
        self.load_mechanisms()


    def load_metadata(self):
        with open(self.path / "map.json", "r") as f:
            map_metadata = json.load(f)
            self.tileset_img = map_metadata['tileset_image']
            self.tileset_cols = map_metadata['tileset_columns']
            self.tileset_rows = map_metadata['tileset_rows']
            self.tile_size = map_metadata['tile_size']
            self.bg_img_path = map_metadata['background_image']
            self.water_tiles = set(map_metadata['water_tiles'])
            self.lava_tiles = set(map_metadata['lava_tiles'])
            self.mechanisms_data = map_metadata['mechanisms']


    def load_tiles(self):
        image = pygame.image.load(self.tileset_img)
        for y in range(self.tileset_rows):
            for x in range(self.tileset_cols):
                original = image.subsurface((x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                scaled = pygame.transform.scale(original, (self.tile_size * self.scale, self.tile_size * self.scale))
                self.tiles.append(scaled)


    def load_map(self):
        # Load background
        self.bg_img = pygame.image.load(self.bg_img_path)

        # Load tiles
        map_details = self.read_csv()
        for y, row in enumerate(map_details):
            for x, tile in enumerate(row):
                tile_idx = int(tile)
                if tile_idx >= 0:
                    if tile_idx in self.lava_tiles:
                        self.lava.add(self.tiles[tile_idx], x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                    elif tile_idx in self.water_tiles:
                        self.water.add(self.tiles[tile_idx], x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                    else:
                        tile_obj = Tile(self.tiles[tile_idx], x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                        self.tiles_group.add(tile_obj)
                        self.tile_rects.append(tile_obj.rect)


    def load_mechanisms(self):
        for data in self.mechanisms_data:
            mechanism = Mechanism()
            for trigger in data['triggers']:
                mechanism.add_trigger(self.tiles[trigger['tile']], trigger['x'] * self.tile_size * self.scale, trigger['y'] * self.tile_size * self.scale)
            for barrier in data['barriers']:
                mechanism.add_barrier(self.tiles[barrier['tile']], barrier['x'] * self.tile_size * self.scale, barrier['y'] * self.tile_size * self.scale)
            self.mechanisms.append(mechanism)
            Locator.add(Mechanism, mechanism)


    def read_csv(self):
        map_details = []
        with open(self.path / "map.csv") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                map_details.append(row)
        return map_details


    def get_rects(self):
        return self.tile_rects
    

    def get_bg(self, width, height):
        return pygame.transform.scale(self.bg_img, (width, height))


    def draw(self, display: pygame.surface.Surface):
        self.tiles_group.draw(display)
        for mechanism in self.mechanisms:
            mechanism.draw(display)


    def draw_fluids(self, display: pygame.surface.Surface):
        self.water.draw(display)
        self.lava.draw(display)