from game.sprites.laser import Laser
from pygame import Surface

from .ship import Ship


class Player(Ship):
    def __init__(self, surface: Surface) -> None:
        super().__init__(surface)
        self.movement_speed = 10.0
        self.health: int = 6

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
        if (self.x + self.image.get_width()) + self.movement_speed > self.screen_dims[
            0
        ]:
            # aligns player with right side of screen boundary
            self.x = self.screen_dims[0] - self.image.get_width()
            self.rect.x = int(self.x)

        # else the player moves to the right
        else:
            self.x += self.movement_speed
            self.rect.x = int(self.x)

    def create_laser(self):
        super().create_laser(-1, (self.rect.top - Laser.w_h[1]))

    def update(self):
        if self.moving_left:
            self.__move_left()
        elif self.moving_right:
            self.__move_right()
        super().update()

        self.lasers.update()
