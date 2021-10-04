import pygame
from pygame.constants import SRCALPHA

from ...sprites import Enemy, Player
from ..background import Background
from ..screen_base import ScreenBase
from ...asset_manager import AssetManager


class LevelOne(ScreenBase):
    def __init__(self, w_h: tuple) -> None:
        self.width, self.height = w_h
        self.image = pygame.Surface(w_h, SRCALPHA)
        self.rect = self.image.get_rect()

        self.background = Background((self.width, self.height))

        self.sprite_images = AssetManager.get_sprite_images()
        self.enemy = Enemy(self.sprite_images["enemy_ship"])
        self.enemy.set_position(self.width / 2 - self.enemy.rect.width / 2, 0.0)

        self.player = Player(self.sprite_images["player_ship"])

        self.player.set_position(
            self.width / 2 - self.player.rect.width / 2,
            self.height - self.player.rect.height,
        )

        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        pygame.time.set_timer(self.enemy.basic_attack, 1000)
        pygame.time.set_timer(self.enemy.special_attack, 2500)

    def __check_collisions(self):
        """check for collision between sprites"""
        # runs method and assigns result to variable
        if p_lasers := pygame.sprite.spritecollide(
            self.enemy, self.player.lasers, True
        ):
            for laser in p_lasers:
                self.enemy.take_damage(laser.damage)

        if e_lasers := pygame.sprite.spritecollide(
            self.player, self.enemy.lasers, True
        ):
            for laser in e_lasers:
                self.player.take_damage(laser.damage)
            # if players health = zero return to main menu
            if self.player.health == 0:
                # disable timer
                pygame.time.set_timer(self.enemy.basic_attack, 0)
                # how to change the screen
                self.change_screen = True
                self.new_screen = "main_menu"

    def __player_keydown_controller(self, event):
        """respond to player inputs"""

        if event.key == pygame.K_a:
            self.player.moving_left = True

        elif event.key == pygame.K_d:
            self.player.moving_right = True

    def __player_keyup_controller(self, event):

        if event.key == pygame.K_a:
            self.player.moving_left = False

        elif event.key == pygame.K_d:
            self.player.moving_right = False

    def __update_game_objects(self):
        """updates and displays game objects"""
        self.background.update()
        self.player.update()
        self.__check_collisions()
        if self.enemy.health > 0:
            self.enemy.update(play_x=self.player.rect.centerx)

    def __draw_game_objects(self):
        self.image.blit(self.background.image, self.background.rect)
        self.image.blit(self.player.image, self.player.rect)
        if self.enemy.health > 0:
            self.image.blit(self.enemy.image, self.enemy.rect)
            for laser in self.enemy.lasers:
                if laser.rect.y > self.height:
                    self.enemy.lasers.remove(laser)

                self.image.blit(laser.image, laser.rect)

        for laser in self.player.lasers:
            if laser.rect.bottom < 0:
                self.player.lasers.remove(laser)

            self.image.blit(laser.image, laser.rect)

    def check_events(self, event):
        """Check level events"""
        if event.type == pygame.KEYDOWN:
            self.__player_keydown_controller(event)

        elif event.type == pygame.KEYUP:
            self.__player_keyup_controller(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.player.create_laser()

        if event.type == self.enemy.basic_attack and self.enemy.health > 0:
            self.enemy.create_laser()
        if event.type == self.enemy.special_attack and self.enemy.health > 0:
            self.enemy.create_special_laser()

    def update(self):
        """Update level elements and draw to level's main surface"""
        self.__update_game_objects()
        self.__draw_game_objects()
