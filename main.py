import pygame
from pygame.locals import *

from data.scripts.font import Font
from data.scripts.clock import Clock
from data.scripts.tileset_loader import TileSetManager
from data.scripts.editor_manager import EditorManager
from data.scripts.image_functions import load_image, scale_image_size

class GameWindow:
    def __init__(self):
        pygame.init()

        self.tile_size = [16, 16]
        self.tile_number = [30, 20]
        self.ratio = 2
        self.screen_size = [(self.tile_size[0] * self.tile_number[0]) * self.ratio, (self.tile_size[1] *
                                                                                           self.tile_number[1]) * self.ratio]
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Mini Golf")
        pygame.display.set_icon(load_image('icon.ico'))

        # Display--------------------#
        self.main_display_size = [self.tile_size[0] * self.tile_number[0], self.tile_size[1] * self.tile_number[1]]
        self.main_display = pygame.Surface(self.main_display_size)

        self.mini_map_size = [500, 500]
        self.mini_map_display = pygame.Surface(self.mini_map_size)

        # Clock---------------------#
        self.clock = Clock()

        self.tileset_manager = TileSetManager()
        self.editor_manager = EditorManager()
        self.mini_map_manager = EditorManager()
        self.editor_manager.load_map(self.tileset_manager.tileset_data)
        self.mini_map_manager.load_map(self.tileset_manager.tileset_data)

        self.game = True

    def main_loop(self):
        while self.game:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.fill((0, 0, 0))
            self.main_display.fill((0, 0, 0))
            self.mini_map_display.fill((0, 0, 0))

            self.editor_manager.show_map(self.main_display)

            self.mini_map_manager.change_offset(self.tile_size[0])
            self.mini_map_manager.show_map(self.mini_map_display)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game = False

                if event.type == pygame.KEYDOWN:
                    if event.key == K_a:
                        self.mini_map_manager.shift_x = "right"
                    if event.key == K_f:
                        self.mini_map_manager.shift_x = "left"
                    if event.key == K_e:
                        self.mini_map_manager.shift_y = "top"
                    if event.key == K_d:
                        self.mini_map_manager.shift_y = "bottom"

                if event.type == pygame.KEYUP:
                    if event.key == K_a:
                        self.mini_map_manager.shift_x = None
                    if event.key == K_f:
                        self.mini_map_manager.shift_x = None
                    if event.key == K_e:
                        self.mini_map_manager.shift_y = None
                    if event.key == K_d:
                        self.mini_map_manager.shift_y = None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        pass
                    if event.button == 2:  # mouse wheel click
                        pass
                    if event.button == 3:  # right click
                        pass
                    if event.button == 4:  # anti-clock wise mouse wheel rotation
                        pass
                    if event.button == 5:  # clock wise mouse wheel rotation
                        pass

                if event.type == pygame.MOUSEBUTTONUP:
                    pass

            pygame.draw.rect(self.mini_map_display, (255, 255, 255), (0, 0, *self.mini_map_size), 10)
            self.screen.blit(scale_image_size(self.main_display, *self.screen_size), (0, 0))
            self.screen.blit(scale_image_size(self.mini_map_display, 150, 150), (self.screen_size[0] - 160, 10))
            pygame.display.update()
            self.clock.tick()


if __name__ == "__main__":
    game = GameWindow()
    game.main_loop()
    pygame.quit()
