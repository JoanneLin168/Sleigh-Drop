# settings.py
from os import walk
import pygame

WIDTH, HEIGHT = 800, 600

# houses
house_sizes_units = [x for x in range (1, 8)]
house_size = HEIGHT // 10
house_gap = (house_size * 2) + (house_size // 2)

# clouds
cloud_spawn_chance = 0.5
cloud_storm_chance = 0.1
clouds_spawn_min_score = 5
cloud_size_units = [2, 3, 4]
cloud_size = WIDTH // 10
cloud_gap = (cloud_size * 2) + (cloud_size // 2)

# world scrolling
world_shift_speed = -2 # this with gradually get faster over time
world_shift_acceleration = -0.0001

# player
player_start_pos = (250, HEIGHT//2)
player_size = 30
max_health = 5
animation_delay = 7
follow_strength = 0.1
max_speed = 5
drop_cooldown = 0  # ms

# present
present_speed = 15

def import_sprite(path):
    surface_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = f"{path}/{image}"
            img_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(img_surface)
    return surface_list