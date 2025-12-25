import pygame

class House(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, good):
        super().__init__()
        self.width = width
        img_path = 'assets/terrain/pipe.png'
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft = pos)
        self.passed = False
        self.good = good

        if not self.good:
                self._apply_red_tint()

    def _apply_red_tint(self):
        # Create a red tint surface
        tint = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)

        # (R, G, B, A) — lower G/B = stronger red
        tint.fill((255, 120, 120, 255))

        # Multiply colours (keeps texture detail)
        self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # update object position due to world scroll
    def update(self, x_shift):
        self.rect.x += x_shift

        # removes the house in the game screen once it is not shown in the screen anymore
        if self.rect.right < (-self.width):
            self.kill()