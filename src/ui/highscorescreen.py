import pygame
from src.settings import WIDTH, HEIGHT

class HighscoreScreen:
    def __init__(self, screen, highscores):
        self.screen = screen
        self.highscores = highscores
        self.title_font = pygame.font.SysFont(None, 64)
        self.entry_font = pygame.font.SysFont(None, 36)
        self.back_button = None  # optional button

    def set_back_button(self, button):
        self.back_button = button

    def update(self):
        self.screen.fill((20, 20, 50))

        # Title
        title_surf = self.title_font.render("Highscores", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 80)))

        # Draw entries
        for i, entry in enumerate(self.highscores):
            text = f"{i+1}. {entry['datetime']} - {entry['score']}"
            text_surf = self.entry_font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surf, (WIDTH // 2 - 150, 150 + i * 40))

        # Back button
        if self.back_button:
            self.back_button.draw(self.screen)

    def handle_event(self, event):
        if self.back_button and self.back_button.is_clicked(event):
            return "back"
        return None
