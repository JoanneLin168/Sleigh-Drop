# main.py
import pygame, sys
from settings import WIDTH, HEIGHT, world_shift_speed
from world import World

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sleigh Drop")

class Main:
    def __init__(self, screen):
        self.screen = screen
        self.bg_img = pygame.image.load('assets/terrain/bg.png')
        self.bg_img = pygame.transform.scale(self.bg_img, (WIDTH, HEIGHT))

        self.ground_scroll = 0
        self.scroll_speed = world_shift_speed
        self.FPS = pygame.time.Clock()
        self.stop_ground_scroll = False

        # Apply dark blue overlay to both bg and ground
        overlay = pygame.Surface((WIDTH+300, HEIGHT), pygame.SRCALPHA) # add extra width to cover scrolling
        overlay.fill((30, 30, 80, 150))  # dark blue overlay
        self.bg_img.blit(overlay, (0, 0))

    def main(self):
        world = World(screen)
        while True:
            self.screen.blit(self.bg_img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if not world.playing and not world.game_over:
                        world.playing = True
                    if event.key == pygame.K_SPACE and not world.game_over:
                        world.playing = True
                    if event.key == pygame.K_r:
                        world.update("restart")
                elif event.type == pygame.MOUSEBUTTONDOWN and world.playing:
                    if event.button == 1:
                        world.update("shoot")

            world.update()
            pygame.display.update()
            self.FPS.tick(60)

if __name__ == "__main__":
    play = Main(screen)
    play.main()