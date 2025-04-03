import pygame
import math


class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.clicked = False
        self.color = (255, 255, 255)
        self.angle = 0
        self.distance = 0
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.power = 0
        self.released = False
        self.deacceraltion = 1
        self.release_time = 0
        self.time_elapsed = 0

    def set_pos(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def change_offset(self, offset):
        self.x -= offset[0]
        self.y -= offset[1]

    def release_player(self):
        if self.released:
            self.angle = self.angle
            time = pygame.time.get_ticks()

            self.time_elapsed = (time - self.release_time) // 300

            power = max(0, self.power - self.time_elapsed)

            self.released = False if power == 0 else True

            coors = self.find_coordinates(power, math.radians(self.angle))

            self.x += coors[0]
            self.y += coors[1]

    def get_distance(self, mouse_pos, pos):
        y = (mouse_pos[1] - pos[1]) ** 2
        x = (mouse_pos[0] - pos[0]) ** 2

        distance = int(math.sqrt(y + x))
        distance /= 2

        if distance > 80:
            distance = 80

        self.power = distance // 10

        return distance

    def find_coordinates(self, distance, angle):
        # angle = angle * math.pi / 180
        y = distance * math.sin(angle)
        x = distance * math.cos(angle)

        return x, y

    def draw_line(self, display, coor):
        pygame.draw.line(display, (255, 0, 0), (self.x, self.y), (self.x - coor[0], self.y - coor[1]), 3)
        pygame.draw.line(display, (255, 0, 0), (self.x, self.y), (self.x + coor[0] // 2, self.y + coor[1] // 2))

    def display(self, display, mouse_pos):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(display, (self.color[0] - 50, self.color[0] - 50, self.color[0] - 50), (self.x, self.y),
                           self.radius - 1)
        pygame.draw.circle(display, (self.color[0] - 100, self.color[0] - 100, self.color[0] - 100), (self.x, self.y),
                           self.radius - 3)

        if self.clicked and not self.released:
            x = mouse_pos[0] - self.x
            y = mouse_pos[1] - self.y
            angle = math.atan2(y, x)

            self.angle = math.degrees(angle) + 180

            self.distance = self.get_distance(mouse_pos, [self.x, self.y])
            coors = self.find_coordinates(self.distance, math.radians(self.angle))

            self.draw_line(display, coors)

        self.release_player()