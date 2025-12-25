# settings.py
from os import walk
import pygame

WIDTH, HEIGHT = 800, 600

# pipes
house_sizes_units = [x for x in range (1, 8)]
house_size = HEIGHT // 10
house_gap = (house_size * 2) + (house_size // 2)
ground_space = 50

# world scrolling
world_shift_speed = -3 # this with gradually get faster over time
world_shift_acceleration = -0.001

# player
max_health = 5
animation_delay = 3
follow_strength = 0.1
max_speed = 5
drop_cooldown = 0  # ms

def import_sprite(path):
    surface_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = f"{path}/{image}"
            img_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(img_surface)
    return surface_list