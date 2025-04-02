import pygame
from data.scripts.file_manager import read_json
from data.scripts.image_functions import load_image, clip_surface, scale_image_ratio


def tileset_loader(folder_name, tileset_name, tile_width, tile_height, tile_space=0):
    tileset_image = load_image(f"{folder_name}/{tileset_name}.png")
    tileset = []
    tileset_width = tileset_image.get_width()
    tileset_height = tileset_image.get_height()
    pos_x, pos_y = 0, 0

    while pos_y + tile_height <= tileset_height:
        while pos_x + tile_width <= tileset_width:
            tile = clip_surface(tileset_image, pos_x, pos_y, tile_width, tile_height)
            tileset.append(tile)
            pos_x += tile_width + tile_space
        pos_y += tile_height + tile_space
        pos_x = 0

    return tileset


class TileSetManager:
    def __init__(self):
        self.path = "images/tilesets_data.txt"
        self.tileset_data = {}
        self.tileset_names = []
        self.tileset_number = 0
        self.tileset_file_data = read_json(self.path)

        self.load_tilesets()
        self.current_tileset = self.tileset_names[0]
        self.tile = self.tileset_data[self.current_tileset][0]

        self.initial_pos_y = 50
        self.pos_y = self.initial_pos_y
        self.tile_spacing = 20
        self.click = False

        self.ratio = 3

    def change_tileset_number(self, number):
        self.tileset_number += number
        if self.tileset_number < 0:
            self.tileset_number = len(self.tileset_names) - 1
        if self.tileset_number > len(self.tileset_names) - 1:
            self.tileset_number = 0

        self.current_tileset = self.tileset_names[self.tileset_number]
        self.tile = self.tileset_data[self.current_tileset][0]

    def load_tilesets(self):
        self.tileset_file_data = self.tileset_file_data.split('\n')
        for line in self.tileset_file_data[1:]:  # Skip the header
            if not line.strip():
                continue

            tile_data = line.split(' ')
            if len(tile_data) < 5:
                print(f"Skipping invalid line: {line}")
                continue

            try:
                folder, name, width, height, space = (
                    tile_data[0],
                    tile_data[1],
                    int(tile_data[2]),
                    int(tile_data[3]),
                    int(tile_data[4]),
                )
                self.tileset_names.append(name)
                self.tileset_data[name] = tileset_loader(folder, name, width, height, space)
            except ValueError as e:
                print(f"Error parsing line: {line}. {e}")

    def display_tilesets(self, display, text, screen_size, mouse_pos, click):

        for tile_image in self.tileset_data[self.current_tileset]:
            tile = tile_image
            if screen_size[0] - 200 < mouse_pos[0] < screen_size[0] and \
                    self.pos_y - self.tile_spacing // 2 < mouse_pos[1] < self.pos_y + tile.get_height() * self.ratio + self.tile_spacing // 2:
                pygame.draw.rect(display, (0, 149, 239), (0, self.pos_y - self.tile_spacing // 2, 200, tile.get_height() * self.ratio + self.tile_spacing))
                if click:
                    pass
                    self.tile = tile
            display.blit(scale_image_ratio(tile, self.ratio), (10, self.pos_y))
            self.pos_y += tile.get_height() * self.ratio + self.tile_spacing

        self.pos_y = self.initial_pos_y

        header_surface = pygame.Surface((200, 30), pygame.SRCALPHA)
        pygame.draw.rect(header_surface, (0, 149, 239, 128), (0, 0, 200, 30))
        display.blit(header_surface, (0, 0))
        text.display_fonts(display, self.current_tileset, [10, 8], 2)
