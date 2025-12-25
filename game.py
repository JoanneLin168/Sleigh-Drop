import pygame
from settings import WIDTH, HEIGHT

pygame.font.init()

class GameIndicator:
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.SysFont('Bauhaus 93', 60)
		self.inst_font = pygame.font.SysFont('Bauhaus 93', 30)
		self.color = pygame.Color("white")
		self.inst_color = pygame.Color("white")

	def show_score(self, int_score):
		score = self.font.render(str(int_score), True, self.color)
		self.screen.blit(score, (WIDTH // 2, 50))

	def instructions(self):
		inst_text1 = "Press SPACE button to Start,"
		inst_text2 = "Press \"R\" Button to Restart Game."
		inst_text3 = "Click MB1 to Drop Presents."
		ins1 = self.inst_font.render(inst_text1, True, self.inst_color)
		ins2 = self.inst_font.render(inst_text2, True, self.inst_color)
		ins3 = self.inst_font.render(inst_text3, True, self.inst_color)
		self.screen.blit(ins1, (225, 150))
		self.screen.blit(ins2, (200, 180))
		self.screen.blit(ins3, (230, 210))