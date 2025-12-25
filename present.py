import pygame
from settings import present_speed
import random

class Present(pygame.sprite.Sprite):
    def __init__(self, width, pos, size):
        super().__init__()
        idx = random.choice([0, 1, 2])
        img_path = f"assets/presents/{idx}.png"
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=pos)
        self.width = width
        self.scored = False
        self.speed_y = present_speed

    def update(self, x_shift):
        self.rect.x += x_shift
        self.rect.y += self.speed_y

        # removes the pipe in the game screen once it is not shown in the screen anymore
        if self.rect.right < (-self.width):
            self.kill()