import pygame

from ...sprites import Enemy, Player
from ..screen_base import ScreenBase
from ...asset_manager import AssetManager


class LevelOne(ScreenBase):
    def __init__(self) -> None:
        self.sprite_images = AssetManager.get_sprite_images()
        self.enemy = Enemy(self.sprite_images["enemy_ship"])
        self.enemy.set_position(self.width / 2 - self.enemy.rect.width / 2, 0.0)

        self.player = Player(self.sprite_images["player_ship"])

        self.player.set_position(
            self.width / 2 - self.player.rect.width / 2,
            self.height - self.player.rect.height,
        )

        self.sprites = pygame.sprite.Group([self.enemy, self.player])

        self.game_over = pygame.USEREVENT + 3

        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        pygame.time.set_timer(self.enemy.basic_attack, 1000)
        pygame.time.set_timer(self.enemy.special_attack, 2500)

    def __check_collisions(self):
        """check for collision between sprites"""
        # temp way to handle enemy collisions
        if self.enemy.health > 0:
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
            if self.player.health <= 0:
                pygame.time.set_timer(self.enemy.basic_attack, 0)
                pygame.time.set_timer(self.enemy.special_attack, 0)
                pygame.time.set_timer(self.game_over, 1500, True)

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

    def __update(self):
        """updates and displays game objects"""
        self.__check_collisions()
        self.background.update()

        for sprite in self.sprites:
            if sprite.health > 0:
                sprite.update(play_x=self.player.rect.centerx)
            elif sprite.dying:
                sprite.update_particles()

    def __draw(self):
        self.image.blit(self.background.image, self.background.rect)
        for sprite in self.sprites:
            if sprite.health > 0:
                self.image.blit(sprite.image, sprite.rect)
                for laser in sprite.lasers:
                    if 0 - laser.rect.height < laser.rect.y < self.height:
                        self.image.blit(laser.image, laser.rect)
                    else:
                        laser.kill()

            elif sprite.dying:
                # switch to true if any particle still has an alpha > 0
                visible: bool = False
                for particle in sprite.color_particles:
                    if particle.alpha > 0:
                        self.image.lock()
                        for position in particle.positions:
                            pygame.draw.circle(
                                self.image, particle.color, position, particle.radius
                            )
                        self.image.unlock()
                        # a particles alpha is greater than zero
                        # and we have not switched the bool yet
                        if not visible:
                            visible = True
                # if all of the particles have an alpha
                # less than zero remove sprite from all groups
                if not visible:
                    sprite.kill()

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
        if event.type == self.game_over:
            pygame.mouse.set_cursor(pygame.cursors.arrow)
            self.change_screen = True
            self.new_screen = "game_over"

    def update(self):
        """Update level elements and draw to level's main surface"""
        self.__update()
        self.__draw()
