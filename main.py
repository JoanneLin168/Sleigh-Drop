# main.py
import pygame, sys
from settings import WIDTH, HEIGHT, world_shift_speed
from world import World
from ui.button import Button
from ui.menu import Menu
from ui.textscreen import TextScreen

MENU = "menu"
GAME = "game"
TUTORIAL = "tutorial"

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


        # Game states
        self.menu = Menu(screen)
        self.state = MENU
        self.font = pygame.font.SysFont(None, 48)
        self.start_button = Button(
            WIDTH // 2 - 100,
            HEIGHT // 2 - 30,
            200,
            60,
            "Start Game",
            self.font
        )
        tutorial_text = (
            "Welcome to Sleigh Drop!\n"
            "Left click to drop presents.\n"
            "Deliver presents to the correct houses.\n"
            "Do not deliver to bad houses or you lose health.\n"
            "Avoid flying into clouds and houses!\n"
        )
        back_button = Button(
            WIDTH // 2 - 100,
            HEIGHT - 100,
            200,
            50,
            "Back",
            self.font
        )
        self.tutorial = TextScreen(
            screen,
            "How to Play",
            tutorial_text,
            buttons=[(back_button, "back")],
        )

    def main(self):
        world = World(screen)
        while True:
            self.screen.blit(self.bg_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.state == MENU:
                    result = self.menu.handle_event(event)
                    if result == "start": # create game
                        # lock mouse into window
                        pygame.event.set_grab(True)
                        pygame.mouse.set_visible(False)
                        self.world = World(self.screen)
                        self.state = GAME
                    elif result == "tutorial":
                        self.state = TUTORIAL
                elif self.state == TUTORIAL:
                    button_clicked = self.tutorial.handle_event(event)
                    if button_clicked:
                        self.state = MENU

                elif self.state == GAME:
                    result = self.world.handle_event(event)
                    if result == "menu":
                        self.state = MENU
                        # release mouse
                        pygame.event.set_grab(False)
                        pygame.mouse.set_visible(True)


            # Game updates
            if self.state == MENU:
                self.menu.update()

            elif self.state == TUTORIAL:
                self.tutorial.update()

            elif self.state == GAME:
                self.world.update()

            pygame.display.update()
            self.FPS.tick(60)

if __name__ == "__main__":
    play = Main(screen)
    play.main()