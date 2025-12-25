import pygame

class TextBox:
    def __init__(self, rect, font, text, text_color=(255, 255, 255),
                 box_color=(40, 40, 90), border_color=(255, 255, 255),
                 padding=16):

        self.rect = pygame.Rect(rect)
        self.font = font
        self.text = text
        self.text_color = text_color
        self.box_color = box_color
        self.border_color = border_color
        self.padding = padding

        self.lines = self.wrap_text(text)

    def wrap_text(self, text):
        lines = []

        # Split text by newline first
        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            words = paragraph.split(" ")
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] <= self.rect.width - 2 * self.padding:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "

            lines.append(current_line)   # finish paragraph
            lines.append("")             # blank line after newline

        return lines[:-1]  # remove last extra blank line

    def draw(self, screen):
        pygame.draw.rect(screen, self.box_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=10)

        y = self.rect.y + self.padding
        for line in self.lines:
            text_surf = self.font.render(line, True, self.text_color)
            screen.blit(text_surf, (self.rect.x + self.padding, y))
            y += self.font.get_height() + 4
