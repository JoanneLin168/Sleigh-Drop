import pygame
import sys
from src.ui.button import Button
from src.settings import WIDTH, HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont('Bauhaus 93', 72)
        self.font = pygame.font.SysFont(None, 48)

        button_w, button_h = 240, 60
        center_x = WIDTH // 2 - button_w // 2

        self.start_btn = Button(center_x, 260, button_w, button_h, "Start Game", self.font)
        self.highscore_btn = Button(center_x, 340, button_w, button_h, "Highscores", self.font)
        self.tutorial_btn = Button(center_x, 420, button_w, button_h, "Tutorial", self.font)
        self.exit_btn = Button(center_x, 500, button_w, button_h, "Exit", self.font)

    def update(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 30, 80, 150))
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("Sleigh Drop", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 160)))

        self.start_btn.draw(self.screen)
        self.highscore_btn.draw(self.screen)
        self.tutorial_btn.draw(self.screen)
        self.exit_btn.draw(self.screen)

    def handle_event(self, event):
        if self.start_btn.is_clicked(event):
            return "start"
        
        if self.highscore_btn.is_clicked(event):
            return "highscore"

        if self.tutorial_btn.is_clicked(event):
            return "tutorial"

        if self.exit_btn.is_clicked(event):
            pygame.quit()
            sys.exit()

        return None
