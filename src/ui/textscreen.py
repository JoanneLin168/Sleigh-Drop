import pygame
from src.ui.textbox import TextBox
from src.settings import WIDTH, HEIGHT

class TextScreen:
    def __init__(self, screen, title, text, buttons=None):
        self.screen = screen

        self.title_font = pygame.font.SysFont('Bauhaus 93', 64)
        self.body_font = pygame.font.SysFont(None, 32)

        self.title = title

        box_rect = (100, 180, WIDTH - 200, HEIGHT - 320)
        self.textbox = TextBox(box_rect, self.body_font, text)

        # buttons = [(Button, response), ...]
        self.buttons = buttons if buttons else []

    def update_text(self, new_text):
        self.textbox.text = new_text
        self.textbox.lines = self.textbox.wrap_text(new_text)

    def update(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 30, 80, 150))
        self.screen.blit(overlay, (0, 0))

        title_surf = self.title_font.render(self.title, True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 100)))

        self.textbox.draw(self.screen)

        for button, _ in self.buttons:
            button.draw(self.screen)

    def handle_event(self, event):
        for button, response in self.buttons:
            if button.is_clicked(event):
                return response
        return None
