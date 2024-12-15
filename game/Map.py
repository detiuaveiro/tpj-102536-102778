import pygame
import csv
from pathlib import Path
import json
import random

from game.consts import SCALE, MAP_FILE, MAP_METADATA
from utils import Locator
from entities import Fluid, Mechanism, Portal
from sprites import Tile


class Map:
    
    def __init__(self, map_folder):
        self.path = Path(map_folder)
        self.map_size = None
        self.tileset_img = None
        self.tileset_cols = None
        self.tileset_rows = None
        self.tile_size = None
        self.scaled_tile_size = None

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
        with open(self.path / MAP_METADATA, "r") as f:
            map_metadata = json.load(f)
            
            # Tileset info
            self.tileset_img = map_metadata['tileset_image']
            self.tileset_cols = map_metadata['tileset_columns']
            self.tileset_rows = map_metadata['tileset_rows']
            self.tile_size = map_metadata['tile_size']
            self.scaled_tile_size = self.tile_size * SCALE
            
            # Special tiles info
            self.water_tiles = set(map_metadata['water_tiles'])
            self.lava_tiles = set(map_metadata['lava_tiles'])
            self.portal_tiles = set(map_metadata['portal_tiles'])
            
            # Mechanisms data
            self.mechanisms_data = map_metadata['mechanisms']
            
            # Background and decoration
            self.background_color = map_metadata['background_color']
            self.decoration_img = map_metadata['decoration_image']
            self.total_decorations = map_metadata['total_decorations']
            
            # Map size
            self.map_size = (
                map_metadata['map_columns'] * self.scaled_tile_size,
                map_metadata['map_rows'] * self.scaled_tile_size
            )
            
            # Players' starting positions
            for player_pos in map_metadata['players_start']:
                x = player_pos['x'] * self.scaled_tile_size
                y = player_pos['y'] * self.scaled_tile_size
                self.players_start.append((x, y))


    def load_tiles(self):
        image = pygame.image.load(self.tileset_img)

        for row in range(self.tileset_rows):
            for col in range(self.tileset_cols):
                original_tile = image.subsurface(
                    (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                )
                scaled_tile = pygame.transform.scale(original_tile, (self.scaled_tile_size, self.scaled_tile_size))
                self.tiles.append(scaled_tile)


    def load_map(self):
        map_details = self.read_map_csv()

        for row_idx, row in enumerate(map_details):
            for col_idx, tile in enumerate(row):
                tile_idx = int(tile)
                if tile_idx >= 0:
                    x_pos = col_idx * self.scaled_tile_size
                    y_pos = row_idx * self.scaled_tile_size
                    
                    if tile_idx in self.lava_tiles:
                        self.lava.add(self.tiles[tile_idx], x_pos, y_pos)
                    elif tile_idx in self.water_tiles:
                        self.water.add(self.tiles[tile_idx], x_pos, y_pos)
                    elif tile_idx in self.portal_tiles:
                        self.portal.add(self.tiles[tile_idx], x_pos, y_pos)
                    else:
                        tile_obj = Tile(self.tiles[tile_idx], x_pos, y_pos)
                        self.tiles_group.add(tile_obj)
                        self.tile_rects.append(tile_obj.rect)
                        Locator.add_collidable(tile_obj)


    def load_mechanisms(self):
        for data in self.mechanisms_data:
            mechanism = Mechanism()
            
            # Add triggers to the mechanism
            for trigger in data['triggers']:
                tile = self.tiles[trigger['tile']]
                x_position = trigger['x'] * self.scaled_tile_size
                y_position = trigger['y'] * self.scaled_tile_size
                mechanism.add_trigger(tile, x_position, y_position)
            
            # Add barriers to the mechanism
            for barrier in data['barriers']:
                tile = self.tiles[barrier['tile']]
                x_position = barrier['x'] * self.scaled_tile_size
                y_position = barrier['y'] * self.scaled_tile_size
                mechanism.add_barrier(tile, x_position, y_position)
            
            self.mechanisms.append(mechanism)
            Locator.add_collidable(mechanism)
        

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


    def read_map_csv(self):
        map_details = []
        with open(self.path / MAP_FILE) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                map_details.append(row)
        return map_details
    

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