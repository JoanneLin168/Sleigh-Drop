import pygame
from src.entities.house import House
from src.entities.cloud import Cloud
from src.entities.player import Player
from src.game import GameIndicator
from src.highscores import update_highscores
from src.settings import *

from src.entities.present import Present
import random
import sys

class World:
    def __init__(self, screen):
        self.screen = screen
        self.world_shift = 0
        self.current_x = 0
        self.current_house = None
        self.houses = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.clouds_storm = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self._generate_world()
        self.playing = True
        self.game_over = False
        self.score_handled = False
        self.game = GameIndicator(screen)
        self.presents = pygame.sprite.Group()

        self.distance_since_last_house = 0
        self.next_house_distance = random.randint(250, 450)

    # creates the player and the obstacle
    def _generate_world(self):
        player = Player(player_start_pos, player_size)
        self.player.add(player)
        self._add_house()

    # adds house once the last house added reached the desired house horizontal spaces
    def _add_house(self):
        house_size_rnd = random.choice(house_sizes_units)
        house_good = random.choice([True, False])
        house_width = house_size_rnd * house_size

        house = House((WIDTH, house_width + house_gap), house_size, HEIGHT, house_good)
        self.houses.add(house)

        self._update_current_house()

        # Only add cloud if the house size is small enough (to allow player to pass)
        if house_size_rnd <= 4 and random.random() < cloud_spawn_chance:
            self._add_cloud()

    # adds cloud
    def _add_cloud(self):
        # Only add cloud if score is high enough
        if self.player.sprite.score > clouds_spawn_min_score:
            cloud_size_rnd = random.choice(cloud_size_units)
            cloud_width = cloud_size_rnd * cloud_size
            cloud_pos = (WIDTH, random.randint(50, HEIGHT // 3))
            cloud_storm = random.random() < cloud_storm_chance

            cloud = Cloud(cloud_pos, cloud_width, cloud_size, cloud_storm)

            if cloud_storm:
                self.clouds_storm.add(cloud)
            else:
                self.clouds.add(cloud)

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
        for cloud in self.clouds:
            if cloud.collides_with(self.player.sprite.rect):
                player.health -= 1
                cloud.kill()  # remove cloud after hit
                break
        for cloud in self.clouds_storm:
            if cloud.collides_with(self.player.sprite.rect):
                self.playing = False
                self.game_over = True
                self.player.sprite.health = 0
                break


        # Increment score if passed a bad house
        if player.rect.x >= self.current_house.rect.centerx and not self.current_house.good:
            player.score += 1
            self.current_house.passed = True
            self._update_current_house()
        

    def _spawn_present(self):
        player = self.player.sprite
        present = Present(WIDTH, player.rect.center, 30)
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

    def _draw_health_bar(self, surface, x, y, health, max_health):
        BAR_WIDTH = 150
        BAR_HEIGHT = 16

        ratio = health / max_health

        bg_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, BAR_WIDTH * ratio, BAR_HEIGHT)

        pygame.draw.rect(surface, (60, 60, 60), bg_rect)
        pygame.draw.rect(surface, (220, 50, 50), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, 2)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and self.playing:
            if event.button == 1:
                self.update("shoot")

        elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
            if event.button == 1:
                result = self.game.gameover_screen.handle_event(event)
                if result == "restart":
                    self.update("restart")
                elif result == "menu":
                    return "menu"

    # updates the player's overall state
    def update(self, player_event = None):
        # applying game physics
        self._scroll_x()
        self._handle_collisions()
        self._check_present_scoring()

        # Check health bar
        if self.player.sprite.health <= 0:
            self.playing = False
            self.game_over = True

        # Controls
        if player_event == "shoot" and not self.game_over:
            player_event = True
            if self.player.sprite.drop_present():
                self._spawn_present()
        elif player_event == "restart":
            self.game_over = False
            self.score_handled = False
            self.houses.empty()
            self.player.empty()
            self.clouds.empty()
            self.clouds_storm.empty()
            self.presents.empty()
            self.player.score = 0
            self.current_house = None
            self._generate_world()
            self.playing = True
        else:
            player_event = False

        # configuring player actions
        if self.playing:
            self.player.sprite.move()
            self._draw_health_bar(
                self.screen,
                x=20,
                y=20,
                health=self.player.sprite.health,
                max_health=max_health
            )
            
            # lock mouse
            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)

        # New house adder
        self.distance_since_last_house += abs(self.world_shift)
        if self.distance_since_last_house >= self.next_house_distance:
            self._add_house()
            self.distance_since_last_house = 0
            self.next_house_distance = random.randint(200, 500)

        # Drawing sprites
        self.houses.update(self.world_shift)
        self.houses.draw(self.screen)
        self.clouds.update(self.world_shift // 2)  # Clouds move slower
        self.clouds.draw(self.screen)
        self.clouds_storm.update(self.world_shift // 2)  # Clouds move slower
        self.clouds_storm.draw(self.screen)
        self.player.update(player_event)
        self.player.draw(self.screen)
        self.presents.update(self.world_shift)
        self.presents.draw(self.screen)
        for particle in self.player.sprite.particles:
            particle.draw(self.screen)

        if self.playing:
            self.game.show_score(self.player.sprite.score)

        # Game Over screen
        if self.game_over:
            # unlock mouse
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)

            if not self.score_handled:
                update_highscores(self.player.sprite.score)
                self.score_handled = True
            self.game.show_gameover(self.player.sprite.score)

        # # Debugging
        # for cloud in self.clouds:
        #     cloud.draw_hitboxes(self.screen)
        # for cloud in self.clouds_storm:
        #     cloud.draw_hitboxes(self.screen)