import pygame
from src.settings import WIDTH, HEIGHT
from src.ui.textscreen import TextScreen
from src.ui.button import Button

from src.highscores import update_highscores

pygame.font.init()

class GameIndicator:
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.SysFont(None, 48)
		self.score_font = pygame.font.SysFont('Bauhaus 93', 60)
		self.score_color = pygame.Color("white")

		# Game Over screen
		gameover_text = (
			"Your score: "
		)
		restart_button = Button(
            WIDTH // 2 - 220,
            HEIGHT - 100,
            200,
            50,
            "Retry",
            self.font
        )
		menu_button = Button(
			WIDTH // 2 + 20,
			HEIGHT - 100,
			200,
			50,
			"Menu",
			self.font
		)
		self.gameover_screen = TextScreen(
			self.screen,
			"Game Over!",
			gameover_text,
			buttons=[
				(menu_button, "menu"),
				(restart_button, "restart")
			]
		)

	def show_score(self, int_score):
		score = self.score_font.render(str(int_score), True, self.score_color)
		self.screen.blit(score, (WIDTH // 2, 50))

	def show_gameover(self, int_score):
		self.gameover_screen.update_text(f"Your score: {int_score}")
		self.gameover_screen.update()
