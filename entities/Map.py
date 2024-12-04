import pygame
import csv
from pathlib import Path
import json
import random

from utils import Locator
from entities import Fluid, Mechanism, Portal
from sprites import Tile


class Map:
    def __init__(self, map_folder, scale):
        self.path = Path(map_folder)
        self.scale = scale
        self.map_size = None
        self.tileset_img = None
        self.tileset_cols = None
        self.tileset_rows = None
        self.tile_size = None
        self.tiles = []
        self.tile_rects = []
        self.tiles_group = pygame.sprite.Group()
        self.total_decorations = 0
        self.decoration_img = None
        self.background_color = None
        self.background = None
        self.water = Fluid("water")
        self.lava = Fluid("lava")
        self.portal = Portal()
        self.mechanisms = []
        self.players_start = []
        
        self.load_metadata()
        self.load_tiles()
        self.load_map()
        self.generate_background()
        self.load_mechanisms()


    def load_metadata(self):
        with open(self.path / "map.json", "r") as f:
            map_metadata = json.load(f)
            self.tileset_img = map_metadata['tileset_image']
            self.tileset_cols = map_metadata['tileset_columns']
            self.tileset_rows = map_metadata['tileset_rows']
            self.tile_size = map_metadata['tile_size']
            self.water_tiles = set(map_metadata['water_tiles'])
            self.lava_tiles = set(map_metadata['lava_tiles'])
            self.portal_tiles = set(map_metadata['portal_tiles'])
            self.mechanisms_data = map_metadata['mechanisms']
            self.decoration_img = map_metadata['decoration_image']
            self.total_decorations = map_metadata['total_decorations']
            self.background_color = map_metadata['background_color']
            self.map_size = (
                map_metadata['map_columns'] * self.tile_size * self.scale,
                map_metadata['map_rows'] * self.tile_size * self.scale
            )
            for i, player in enumerate( map_metadata['players_start']):
                x = player['x'] * self.tile_size * self.scale
                y = player['y'] * self.tile_size * self.scale
                self.players_start.append((x, y))


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
                    if tile_idx in self.lava_tiles:
                        self.lava.add(self.tiles[tile_idx], x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                    elif tile_idx in self.water_tiles:
                        self.water.add(self.tiles[tile_idx], x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                    elif tile_idx in self.portal_tiles:
                        self.portal.add(self.tiles[tile_idx], x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                    else:
                        tile_obj = Tile(self.tiles[tile_idx], x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                        self.tiles_group.add(tile_obj)
                        self.tile_rects.append(tile_obj.rect)
                        Locator.add_collidable(tile_obj)


    def load_mechanisms(self):
        for data in self.mechanisms_data:
            mechanism = Mechanism()
            for trigger in data['triggers']:
                mechanism.add_trigger(self.tiles[trigger['tile']], trigger['x'] * self.tile_size * self.scale, trigger['y'] * self.tile_size * self.scale)
            for barrier in data['barriers']:
                mechanism.add_barrier(self.tiles[barrier['tile']], barrier['x'] * self.tile_size * self.scale, barrier['y'] * self.tile_size * self.scale)
            self.mechanisms.append(mechanism)
            Locator.add_collidable(mechanism)


    def read_csv(self):
        map_details = []
        with open(self.path / "map.csv") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                map_details.append(row)
        return map_details
    

    def generate_background(self):
        background = pygame.Surface(self.map_size)
        background.fill(self.background_color)
        decoration = pygame.image.load(self.decoration_img)
        w, h = decoration.get_size()

        for _ in range(self.total_decorations):
            x = random.randint(0, self.map_size[0] - w)
            y = random.randint(0, self.map_size[1] - h)
            background.blit(decoration, (x, y))

        self.background = background


    def get_rects(self):
        return self.tile_rects
    

    def get_map_size(self):
        return self.map_size
    

    def get_players_start(self):
        return self.players_start


    def draw(self, display: pygame.surface.Surface):
        display.blit(self.background, (0, 0))
        self.tiles_group.draw(display)
        self.portal.draw(display)
        for mechanism in self.mechanisms:
            mechanism.draw(display)


    def draw_fluids(self, display: pygame.surface.Surface):
        self.water.draw(display)
        self.lava.draw(display)