import pygame
import random

class SnowParticle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-self.screen_height, 0)
        self.speed_y = random.uniform(0.5, 2.0)
        self.speed_x = random.uniform(-0.3, 0.3)
        self.radius = random.randint(1, 3)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.y > self.screen_height:
            self.reset()

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            (230, 240, 255),
            (int(self.x), int(self.y)),
            self.radius
        )