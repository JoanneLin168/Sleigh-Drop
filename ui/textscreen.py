import pygame
from ui.textbox import TextBox
from ui.button import Button
from settings import WIDTH, HEIGHT

class TextScreen:
    def __init__(self, screen, title, text):
        self.screen = screen

        self.title_font = pygame.font.SysFont(None, 64)
        self.body_font = pygame.font.SysFont(None, 32)

        self.title = title

        box_rect = (100, 180, WIDTH - 200, HEIGHT - 320)
        self.textbox = TextBox(box_rect, self.body_font, text)

        self.back_button = Button(
            WIDTH // 2 - 100,
            HEIGHT - 100,
            200,
            50,
            "Back",
            self.body_font
        )

    def update(self):
        self.screen.fill((20, 20, 50))

        title_surf = self.title_font.render(self.title, True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 100)))

        self.textbox.draw(self.screen)
        self.back_button.draw(self.screen)

    def handle_event(self, event):
        if self.back_button.is_clicked(event):
            return "back"
        return None
