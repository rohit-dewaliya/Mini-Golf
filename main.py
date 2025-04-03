import pygame
from pygame.locals import *

from data.scripts.font import Font
from data.scripts.clock import Clock
from data.scripts.editor_manager import EditorManager
from data.scripts.image_functions import load_image, scale_image_size
from data.scripts.player import Player


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

        # Variables-----------------------#
        self.editor_manager = EditorManager()
        self.mini_map_manager = EditorManager()

        self.editor_manager.load_map()
        self.mini_map_manager.load_map()

        self.player = Player(*self.editor_manager.starting_point, 5)

        self.true_scroll = [0, 0]
        self.scroll = [0, 0]

        self.game = True

    def scroll_back(self, obj, delta_time):
        x = self.main_display_size[0] // 2
        y = self.main_display_size[1] // 2
        self.true_scroll[0] += ((obj.x - self.true_scroll[0] - x) / 10) * delta_time
        self.true_scroll[1] += ((obj.y - self.true_scroll[1] - y) / 10) * delta_time

    def main_loop(self):
        while self.game:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = [mouse_pos[0] // self.ratio, mouse_pos[1] // self.ratio]

            self.scroll_back(self.player, 1)
            self.scroll = self.true_scroll.copy()
            self.scroll[0] = int(self.scroll[0])
            self.scroll[1] = int(self.scroll[1])

            self.screen.fill((0, 0, 0))
            self.main_display.fill((110, 170, 130))
            self.mini_map_display.fill((0, 0, 0))

            self.editor_manager.show_map(self.main_display)
            self.editor_manager.apply_offset(self.scroll)

            self.mini_map_manager.change_offset(self.tile_size[0])
            self.mini_map_manager.show_map(self.mini_map_display)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game = False

                if event.type == pygame.KEYDOWN:
                    if event.key == K_a or event.key == K_LEFT:
                        self.mini_map_manager.shift_x = "right"
                    if event.key == K_d or event.key == K_RIGHT:
                        self.mini_map_manager.shift_x = "left"
                    if event.key == K_w or event.key == K_UP:
                        self.mini_map_manager.shift_y = "top"
                    if event.key == K_s or event.key == K_DOWN:
                        self.mini_map_manager.shift_y = "bottom"
                    # if event.type == pygame.KEYDOWN and event.key == K_f:
                    #     pygame.display.toggle_fullscreen()

                if event.type == pygame.KEYUP:
                    if event.key == K_a or event.key == K_LEFT:
                        self.mini_map_manager.shift_x = None
                    if event.key == K_d or event.key == K_RIGHT:
                        self.mini_map_manager.shift_x = None
                    if event.key == K_w or event.key == K_UP:
                        self.mini_map_manager.shift_y = None
                    if event.key == K_s or event.key == K_DOWN:
                        self.mini_map_manager.shift_y = None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        self.player.clicked = True
                    if event.button == 2:  # mouse wheel click
                        pass
                    if event.button == 3:  # right click
                        pass
                    if event.button == 4:  # anti-clock wise mouse wheel rotation
                        pass
                    if event.button == 5:  # clock wise mouse wheel rotation
                        pass

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.player.distance <= 10:
                            self.player.released = False
                        else:
                            self.player.released = True if not self.player.released else False
                        self.player.clicked = False
                        self.player.release_time = pygame.time.get_ticks()


            self.player.display(self.main_display, mouse_pos)
            self.player.change_offset(self.scroll)

            pygame.draw.rect(self.mini_map_display, (255, 255, 255), (0, 0, *self.mini_map_size), 10)
            self.screen.blit(scale_image_size(self.main_display, *self.screen_size), (0, 0))
            self.screen.blit(scale_image_size(self.mini_map_display, 150, 150), (self.screen_size[0] - 160, 10))
            pygame.display.update()
            self.clock.tick()


if __name__ == "__main__":
    game = GameWindow()
    game.main_loop()
    pygame.quit()
