import pygame
from house import House
from player import Player
from game import GameIndicator
from settings import (
    WIDTH, HEIGHT, house_size, house_gap, house_sizes_units,
    world_shift_speed, world_shift_acceleration,
    max_health
)

from present import Present
import random

class World:
    def __init__(self, screen):
        self.screen = screen
        self.world_shift = 0
        self.current_x = 0
        self.current_house = None
        self.houses = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self._generate_world()
        self.playing = False
        self.game_over = False
        # self.passed = True
        self.game = GameIndicator(screen)
        self.presents = pygame.sprite.Group()

        self.distance_since_last_house = 0
        self.next_house_distance = random.randint(250, 450)

    # creates the player and the obstacle
    def _generate_world(self):
        self._add_house()
        player = Player((WIDTH//2 - house_size, HEIGHT//2 - house_size), 30)
        self.player.add(player)

    # adds house once the last house added reached the desired house horizontal spaces
    def _add_house(self):
        house_size_rnd = random.choice(house_sizes_units)
        house_good = random.choice([True, False])
        house_height = house_size_rnd * house_size

        house = House((WIDTH, house_height + house_gap), house_size, HEIGHT, house_good)
        self.houses.add(house)

        self._update_current_house()

    # for moving background/obstacle
    def _scroll_x(self):
        if self.playing:
            if self.world_shift == 0:
                self.world_shift = world_shift_speed
            else:
                self.world_shift += world_shift_acceleration
        else:
            self.world_shift = 0

    # Change self.current_house to be the next one to be passed
    def _update_current_house(self):
        self.current_house = None
        for house in self.houses:
            if not house.passed:
                self.current_house = house
                break

    # handles scoring and collision
    def _handle_collisions(self):
        player = self.player.sprite
        # for collision checking
        if pygame.sprite.groupcollide(self.player, self.houses, False, False) or player.rect.bottom >= HEIGHT or player.rect.top <= 0:
            self.playing = False
            self.game_over = True
            self.player.sprite.health = 0
        else:
            # if player pass through the house gaps
            player = self.player.sprite

        # Increment score if passed a bad house
        if player.rect.x >= self.current_house.rect.centerx and not self.current_house.good:
            player.score += 1
            self.current_house.passed = True
            self._update_current_house()
        

    def _spawn_present(self):
        bird = self.player.sprite
        present = Present(WIDTH, bird.rect.center, 30)
        self.presents.add(present)

    def _check_present_scoring(self):
        for present in self.presents:
            hit_any_house = False
            for house in self.houses:
                # Check if present hits any house
                if (house.rect.left < present.rect.centerx < house.rect.right and present.rect.bottom > house.rect.top):
                    if house.good and not present.scored:
                        self.player.sprite.score += 1
                        present.scored = True
                        present.kill()
                    elif not house.good and not present.scored:
                        self.player.sprite.health -= 1
                        present.scored = True
                        present.kill()

            # Check if present hits the floor
            if present.rect.bottom >= HEIGHT:
                self.player.sprite.health -= 1
                present.kill()

    def draw_health_bar(self, surface, x, y, health, max_health):
        BAR_WIDTH = 150
        BAR_HEIGHT = 16

        ratio = health / max_health

        bg_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, BAR_WIDTH * ratio, BAR_HEIGHT)

        pygame.draw.rect(surface, (60, 60, 60), bg_rect)
        pygame.draw.rect(surface, (220, 50, 50), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, 2)

    # updates the player's overall state
    def update(self, player_event = None):
        # applying game physics
        self._scroll_x()
        self._handle_collisions()
        self._check_present_scoring()

        # configuring player actions
        if not self.playing:
            self.game.instructions()

        # Check health bar
        if self.player.sprite.health <= 0:
            self.playing = False
            self.game_over = True

        if player_event == "shoot" and not self.game_over:
            player_event = True
            if self.player.sprite.drop_present():
                self._spawn_present()
        elif player_event == "restart":
            self.game_over = False
            self.houses.empty()
            self.player.empty()
            self.player.score = 0
            self._generate_world()
        else:
            player_event = False

        if self.playing:
            self.player.sprite.move()

        # new house adder
        self.distance_since_last_house += abs(self.world_shift)
        if self.distance_since_last_house >= self.next_house_distance:
            self._add_house()
            self.distance_since_last_house = 0
            self.next_house_distance = random.randint(200, 500)

        # Drawing sprites
        self.houses.update(self.world_shift)
        self.houses.draw(self.screen)
        self.player.update(player_event)
        self.player.draw(self.screen)
        self.presents.update(self.world_shift)
        self.presents.draw(self.screen)
        self.game.show_score(self.player.sprite.score)
        self.draw_health_bar(
            self.screen,
            x=20,
            y=20,
            health=self.player.sprite.health,
            max_health=max_health
        )