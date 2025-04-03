import pygame
import math

from data.scripts.collision_detection import CollisionCheck, collision_test


class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.clicked = False
        self.color = (255, 255, 255)
        self.angle = 0
        self.distance = 0
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.phy_obj = CollisionCheck(self.x, self.y, self.radius * 2, self.radius * 2)
        self.power = 0
        self.released = False
        self.deacceraltion = 1
        self.release_time = 0
        self.time_elapsed = 0
        self.collided = False
        self.collision_direction = None

    def set_pos(self):
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def change_offset(self, offset):
        self.x -= offset[0]
        self.y -= offset[1]

        self.set_pos()

    def release_player(self, display, platforms, offset):
        if not self.released:
            return

        # Get time elapsed since release
        time = pygame.time.get_ticks()
        self.time_elapsed = (time - self.release_time) // 300

        # Calculate current power with deceleration
        power = max(0, self.power - self.time_elapsed)

        # Stop if power is too low
        if power < 2:
            self.released = False
            self.collision_direction = None
            return

        # Calculate movement vector
        coors = self.find_coordinates(power, math.radians(self.angle))

        # Apply bounce from previous collision if any
        if self.collision_direction:
            if self.collision_direction in ['left', 'right']:
                coors[0] = -coors[0] * 0.8
            elif self.collision_direction in ['top', 'bottom']:
                coors[1] = -coors[1] * 0.8
            # Reset collision direction after applying it
            self.collision_direction = None

        # Move the ball
        new_x = self.x + coors[0]
        new_y = self.y + coors[1]

        # Update rectangle position for collision testing
        test_rect = self.rect.copy()
        test_rect.x = new_x - self.radius
        test_rect.y = new_y - self.radius

        # Check for collisions
        collision_found = False
        for platform in platforms:
            pygame.draw.rect(display, (255, 255, 0), (platform.x, platform.y, platform.width, platform.height))

            if test_rect.colliderect(platform):
                collision_found = True

                # Calculate collision properties
                dx = test_rect.centerx - platform.centerx
                dy = test_rect.centery - platform.centery
                width = (test_rect.width + platform.width) / 2
                height = (test_rect.height + platform.height) / 2
                overlap_x = width - abs(dx)
                overlap_y = height - abs(dy)

                # Determine collision side (smallest overlap)
                if overlap_x > overlap_y:
                    if dy > 0:
                        self.collision_direction = 'top'
                        new_y = platform.bottom + self.radius
                    else:
                        self.collision_direction = 'bottom'
                        new_y = platform.top - self.radius
                else:
                    if dx > 0:
                        self.collision_direction = 'left'
                        new_x = platform.right + self.radius
                    else:
                        self.collision_direction = 'right'
                        new_x = platform.left - self.radius

                print(f"Collision detected: {self.collision_direction}")

                # Reduce power after collision
                self.power *= 0.8
                break

        # Update positions
        self.x = new_x
        self.y = new_y
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

        # Update collision state
        self.collided = collision_found

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

        return [x, y]

    def draw_line(self, display, coor):
        pygame.draw.line(display, (255, 0, 0), (self.x, self.y), (self.x - coor[0], self.y - coor[1]), 3)
        pygame.draw.line(display, (255, 0, 0), (self.x, self.y), (self.x + coor[0] // 2, self.y + coor[1] // 2))

    def display(self, display, mouse_pos, platforms, offset):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(display, (self.color[0] - 50, self.color[0] - 50, self.color[0] - 50), (self.x, self.y),
                           self.radius - 1)
        pygame.draw.circle(display, (self.color[0] - 100, self.color[0] - 100, self.color[0] - 100), (self.x, self.y),
                           self.radius - 3)
        # pygame.draw.rect(display, (0, 0, 0), self.rect)

        if self.clicked and not self.released:
            x = mouse_pos[0] - self.x
            y = mouse_pos[1] - self.y
            angle = math.atan2(y, x)

            self.angle = math.degrees(angle) + 180

            self.distance = self.get_distance(mouse_pos, [self.x, self.y])
            coors = self.find_coordinates(self.distance, math.radians(self.angle))

            self.draw_line(display, coors)

        self.release_player(display, platforms, offset)