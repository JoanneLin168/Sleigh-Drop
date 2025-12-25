import pygame

class Cloud(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, storm=False):
        super().__init__()
        self.width = width
        self.storm = storm

        if self.storm:
            img_path = 'assets/clouds/cloud_storm.png'
        else:
            img_path = 'assets/clouds/cloud.png'
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft = pos)

        # Define two hitboxes
        # Central big square
        w, h = self.rect.width, self.rect.height
        self.hitbox_center = pygame.Rect(
            self.rect.left + w*0.2,  # some inset from sides
            self.rect.top,
            w*0.6,
            h
        )
        # Thin bottom rectangle
        self.hitbox_bottom = pygame.Rect(
            self.rect.left,
            self.rect.top + h*0.4,
            w,
            h*0.6
        )

    def draw_hitboxes(self, surface):
        # Draw center hitbox in red
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox_center, 2)
        # Draw bottom hitbox in blue
        pygame.draw.rect(surface, (0, 0, 255), self.hitbox_bottom, 2)

    # update object position due to world scroll
    def update(self, x_shift):
        self.rect.x += x_shift

        # Update hitboxes position
        self.hitbox_center.x += x_shift
        self.hitbox_bottom.x += x_shift

        # removes the house in the game screen once it is not shown in the screen anymore
        if self.rect.right < (-self.width):
            self.kill()