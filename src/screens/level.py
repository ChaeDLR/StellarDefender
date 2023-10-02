import pygame

from .levels.one import LevelOne
from ..sprites import Player
from ..hud import Hud
from ..base import ScreenBase
from .menus.pause_menu import PauseMenu
from ..surface_components import ProgressBar, TextSurface


class Level(ScreenBase):
    score: float = 0.0
    paused: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.state = LevelOne()
        self.player = Player()

        self.player.set_position(
            self.width / 2 - self.player.rect.width / 2,
            self.height - (self.player.rect.height * 2),
        )

        self.__init_hud()

        self.sprites = pygame.sprite.Group(self.player)
        self.pause_menu = PauseMenu()

        pygame.mouse.set_cursor(pygame.cursors.broken_x)

    def __get_txt(self) -> str:
        return f"{int(self.score)}"

    def __init_hud(self) -> None:
        """initialize players heads up display"""
        self.hud = Hud((self.width, self.height))
        health_bar = ProgressBar(
            (20, 25), (200, 30), (210, 20, 40, 255), self.player.get_healthp
        )
        score = TextSurface((self.width - 260, 25), 56, self.__get_txt)
        self.hud.attach(health_bar, score)
        self.hud.update()

    def __check_collisions(self):
        """check for collision between sprites"""
        for enemy in self.state.group.sprites():
            if enemy.health > 0:
                if p_lasers := pygame.sprite.spritecollide(
                    enemy, self.player.lasers, True
                ):
                    for laser in p_lasers:
                        enemy.take_damage(laser.damage)
                        if enemy.dying:
                            self.score += enemy.points_value
                            self.hud.update()

            if e_lasers := pygame.sprite.spritecollide(self.player, enemy.lasers, True):
                for laser in e_lasers:
                    self.player.take_damage(laser.damage)
                    if self.player.health <= 0:
                        self.next_screen = "game_over"
                        pygame.event.post(pygame.event.Event(self.CHANGESCREEN))
                    self.hud.update()

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
        self.image.blits(self.hud.get_blitseq())

    def check_events(self, event: pygame.event.Event):
        """Check level events"""
        if self.paused:
            if event.type == pygame.KEYUP:
                self.player.keyup_handler(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.player.mouseup_handler(event)

            self.pause_menu.check_events(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(self.PAUSE))
            else:
                self.player.keydown_handler(event)

        elif event.type == pygame.KEYUP:
            self.player.keyup_handler(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.player.mousedown_handler(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.player.mouseup_handler(event)

        else:
            self.state.check_events(event)

        if event.type == self.PAUSE:
            if self.paused:
                self.state.unpause()
                self.paused = False
                pygame.mouse.set_cursor(pygame.cursors.broken_x)
            else:
                self.state.pause()
                self.paused = True
                pygame.mouse.set_cursor(pygame.cursors.arrow)

    def update(self):
        """Update level elements and draw to level's main surface"""
        if self.paused:
            self.pause_menu.update()
            self.__draw()
            self.image.blit(self.pause_menu.image, self.pause_menu.rect)
        else:
            self.__update()
            self.__draw()
