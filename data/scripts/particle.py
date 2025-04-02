import pygame, os
from data.scripts.image_functions import swap_color


def blit_center(surf, surf2, pos):
    x = int(surf2.get_width() / 2)
    y = int(surf2.get_height() / 2)
    surf.blit(surf2, (pos[0] - x, pos[1] - y))


# Particles-------------------------------------------------------------#
def particle_file_sort(l):
    l2 = []
    for obj in l:
        l2.append(int(obj[:-4]))
    l2.sort()
    l3 = []
    for obj in l2:
        l3.append(str(obj) + '.png')
    return l3


global particle_images
particle_images = {}


def load_particle_images(path):
    global particle_images
    e_colorkey = (0, 0, 0)
    file_list = os.listdir(path)
    for folder in file_list:
        try:
            img_list = os.listdir(path + '/' + folder)
            img_list = particle_file_sort(img_list)
            images = []
            for img in img_list:
                images.append(pygame.image.load(path + '/' + folder + '/' + img).convert())
            for img in images:
                img.set_colorkey(e_colorkey)
            particle_images[folder] = images.copy()
        except:
            pass


class Particle(object):

    def __init__(self, loc, particle_type, motion, decay_rate, start_frame, custom_color=None, physics=False):
        self.x = loc[0]
        self.y = loc[1]
        self.type = particle_type
        self.motion = motion
        self.decay_rate = decay_rate
        self.color = custom_color
        self.frame = start_frame
        self.physics = physics
        self.orig_motion = self.motion
        self.temp_motion = [0, 0]
        self.time_left = len(particle_images[self.type]) + 1 - self.frame
        self.render = True

    def draw(self, surface, scroll):
        global particle_images
        if self.render:
            # if self.frame > len(particle_images[self.type]):
            #    self.frame = len(particle_images[self.type])
            if self.color == None:
                blit_center(surface, particle_images[self.type][int(self.frame)],
                            (self.x - scroll[0], self.y - scroll[1]))
            else:
                blit_center(surface,
                            swap_color(particle_images[self.type][int(self.frame)], (255, 255, 255), self.color,
                                       (0, 0, 0)), (self.x - scroll[0], self.y - scroll[1]))

    def update(self, dt):
        self.frame += self.decay_rate * dt
        self.time_left = len(particle_images[self.type]) + 1 - self.frame
        running = True
        self.render = True

        if self.frame >= len(particle_images[self.type]):
            self.render = False
            if self.frame >= len(particle_images[self.type]) + 1:
                running = False

        if not self.physics:
            self.x += (self.temp_motion[0] + self.motion[0]) * dt
            self.y += (self.temp_motion[1] + self.motion[1]) * dt
        self.temp_motion = [0, 0]

        return running