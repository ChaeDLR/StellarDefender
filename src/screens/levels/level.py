import pygame

from .states import LevelOne
from ...sprites import Player
from ..screen_base import ScreenBase
from ..menus.pause_menu import PauseMenu


class Level(ScreenBase):

    __events: list[pygame.event.Event] = []

    paused: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.state = LevelOne()
        self.player = Player()

        self.player.set_position(
            self.width / 2 - self.player.rect.width / 2,
            self.height - self.player.rect.height,
        )

        self.sprites = pygame.sprite.Group(self.player)

        pygame.mouse.set_visible(False)

        self.pause_menu = PauseMenu()

    def __check_collisions(self):
        """check for collision between sprites"""
        for enemy in self.state.group.sprites():
            if enemy.health > 0:
                if p_lasers := pygame.sprite.spritecollide(
                    enemy, self.player.lasers, True
                ):
                    for laser in p_lasers:
                        enemy.take_damage(laser.damage)

            if e_lasers := pygame.sprite.spritecollide(
                    self.player,
                    enemy.lasers,
                    True
                ):
                for laser in e_lasers:
                    self.player.take_damage(laser.damage)
                    if self.player.health <= 0:
                        self.next_screen = "game_over"
                        pygame.event.post(pygame.event.Event(self.CHANGESCREEN))

    def __update(self):
        """updates and displays game objects"""
        self.state.update(player_x=self.player.rect.centerx)
        self.__check_collisions()

        for sprite in self.sprites:
            if sprite.health > 0:
                sprite.update(play_x=self.player.rect.centerx)
            elif sprite.dying:
                sprite.update_particles()

    def __draw(self):
        self.image.fill((0, 0, 0))
        for sprite in [*self.sprites.sprites(), *self.state.group.sprites()]:
            for laser in sprite.lasers:
                if 0 - laser.rect.height < laser.rect.y < self.height:
                    self.image.blit(laser.image, laser.rect)
                else:
                    laser.kill()

            if sprite.health > 0:
                self.image.blit(sprite.image, sprite.rect)
            elif sprite.dying:
                # switch to true if any particle still has an alpha > 0
                visible: bool = False
                for particle in sprite.color_particles:
                    if particle.alpha > 20.0:
                        visible = True
                        for position in particle.positions:
                            pygame.draw.circle(
                                self.image,
                                particle.color,
                                position,
                                particle.radius,
                            )
                # if all of the particles have an alpha
                # less than zero remove sprite from all groups
                if not visible:
                    sprite.kill()

    def __player_keydown_controller(self, event):
        """respond to player inputs"""
        if event.key == pygame.K_SPACE:
            if self.player.health > 0:
                self.player.firing = True

        elif event.key == pygame.K_a:
            self.player.moving_left = True

        elif event.key == pygame.K_d:
            self.player.moving_right = True

    def __player_keyup_controller(self, event):
        if event.key == pygame.K_SPACE:
            self.player.firing = False

        elif event.key == pygame.K_a:
            self.player.moving_left = False

        elif event.key == pygame.K_d:
            self.player.moving_right = False

    def check_events(self, event: pygame.event.Event):
        """Check level events"""
        if self.paused:
            if event.type == pygame.KEYDOWN:
                self.__player_keydown_controller(event)
            elif event.type == pygame.KEYUP:
                self.__player_keyup_controller(event)
            else:
                self.pause_menu.check_events(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(self.PAUSE))
            else:
                self.__player_keydown_controller(event)

        elif event.type == pygame.KEYUP:
            self.__player_keyup_controller(event)

        else:
            self.state.check_events(event)

        if event.type == self.PAUSE:
            if self.paused:
                self.state.unpause()
                self.paused = False
                pygame.mouse.set_visible(False)
            else:
                self.state.pause()
                self.paused = True
                pygame.mouse.set_visible(True)


    def update(self):
        """Update level elements and draw to level's main surface"""
        if self.paused:
            self.pause_menu.update()
            self.__draw()
            self.image.blit(self.pause_menu.image, self.pause_menu.rect)
        else:
            self.__update()
            self.__draw()
