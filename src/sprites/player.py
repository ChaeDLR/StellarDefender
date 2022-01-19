from pygame import time

from .ship import Ship
from .laser import Laser
from ..assets import Assets


class Player(Ship):

    colors: tuple = None

    def __init__(self) -> None:
        super().__init__(Assets.get_image("player"))
        self.base_speed: float = 10.0
        self.movement_speed: float = 10.0
        self.health: int = 6
        self.firing: bool = False
        self.__fire_cd: int = 250  # in milliseconds
        self.__prev_ticks: int = time.get_ticks()

        if not Player.colors:
            Player.colors = self._get_sprite_colors(self.image)

    def __move_left(self):
        """move the player to the left"""
        # checks if player is moving off the screen
        if self.x - self.movement_speed <= 0:
            # aligns player with left of screen
            self.rect.x = 0
            self.x = float(self.rect.x)
        else:
            # moves left
            self.x -= self.movement_speed
            self.rect.x = int(self.x)

    def __move_right(self):
        """move the player to the right"""
        # stops player from moving off the right side of the screen
        if (self.x + self.image.get_width()) + self.movement_speed > self.screen_size[
            0
        ]:
            # aligns player with right side of screen boundary
            self.x = self.screen_size[0] - self.image.get_width()
            self.rect.x = int(self.x)

        # else the player moves to the right
        else:
            self.x += self.movement_speed
            self.rect.x = int(self.x)

    def create_laser(self):
        if self.__fire_cd < (time.get_ticks() - self.__prev_ticks):
            super().create_laser(-1, (self.rect.top - Laser.w_h[1]))
            self.__prev_ticks = time.get_ticks()

    def update_particles(self) -> None:
        super().update_particles()
        self.lasers.update()

    def update(self, **kwargs):
        if self.moving_left:
            self.__move_left()
        elif self.moving_right:
            self.__move_right()
        super().update()

        if self.firing:
            self.create_laser()

        self.lasers.update()
