import random
import pygame
from src.settings import import_sprite
from src.settings import (
	max_health, animation_delay,
	follow_strength, max_speed, drop_cooldown
)
from src.entities.particle import Particle

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, size):
		super().__init__()
		# play basic info
		self.health = max_health
		self.frame_index = 0
		self.animation_delay = animation_delay
		self.follow_strength = follow_strength
		self.max_speed = max_speed
		self.drop_cooldown = drop_cooldown
		self.particles = []
		self.particle_timer = 0

		self.last_drop = pygame.time.get_ticks()

		# player animation
		self.player_img = import_sprite("assets/santa")
		self.image = self.player_img[self.frame_index]
		self.image = pygame.transform.scale(self.image, (size, size))
		self.rect = self.image.get_rect(topleft = pos)
		self.mask = pygame.mask.from_surface(self.image)

		# player status
		self.direction = pygame.math.Vector2(0, 0)
		self.score = 0

	def _emit_trail(self):
		for _ in range(2):  # density
			spawn_pos = (
				self.rect.left,
				self.rect.centery + random.randint(-8, 8) + 5
			)
			self.particles.append(Particle(spawn_pos))

	# for player's flying animation
	def _animate(self):
		sprites = self.player_img
		sprite_index = (self.frame_index // self.animation_delay) % len(sprites)
		self.image = sprites[sprite_index]
		self.frame_index += 1
		self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
		self.mask = pygame.mask.from_surface(self.image)
		if self.frame_index // self.animation_delay > len(sprites):
			self.frame_index = 0
			
	def move(self):
		mouse_y = pygame.mouse.get_pos()[1]
		dy = mouse_y - self.rect.centery

		DEADZONE = 4  # pixels

		if abs(dy) <= DEADZONE:
			# Close enough → stop completely (prevents bouncing)
			self.direction.y = 0
			self.rect.centery = mouse_y
		else:
			# Smooth follow without oscillation
			self.direction.y = dy * self.follow_strength

			# Clamp speed
			self.direction.y = max(
				-self.max_speed,
				min(self.direction.y, self.max_speed)
			)

			self.rect.y += self.direction.y

	def drop_present(self):
		now = pygame.time.get_ticks()
		if now - self.last_drop > self.drop_cooldown:
			self.last_drop = now
			return True
		return False

	def update(self, player_event = None):
		if self.health > 0:
			self._animate()
			self._emit_trail()

		# Update particles
		for particle in self.particles[:]:
			particle.update()
			if particle.life <= 0:
				self.particles.remove(particle)

