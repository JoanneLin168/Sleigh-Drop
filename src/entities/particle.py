import pygame
import random

class Particle:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(
            random.uniform(-0.5, -2.0),   # drift left
            random.uniform(-0.5, 0.5)     # slight vertical spread
        )
        self.life = random.randint(80, 100)
        self.radius = random.randint(1, 3)

    def update(self):
        self.pos += self.vel
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / 100))
            surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (220, 240, 255, alpha),  # icy white-blue
                (self.radius, self.radius),
                self.radius
            )
            surface.blit(surf, self.pos)
