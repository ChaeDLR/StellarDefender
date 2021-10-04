from pygame import sprite
from ..settings import screen_dims
from .laser import Laser


class Ship(sprite.Sprite):
    """
    A base class for all of the ship sprites
    """

    def __init__(self, surface: dict):
        super().__init__()
        self.screen_dims = screen_dims

        self.image = surface["image"]
        self.rect = self.image.get_rect()
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.colors = surface["colors"]

        self.moving_left, self.moving_right = False, False
        self.movement_speed: float = 5.5
        self.alpha: int = 255
        self.alpha_switch: int = 1
        self.animation_counter: int = 1
        self.side_switch: bool = True
        self.damaged: bool = False

        self.lasers = sprite.Group()

    def __animate(self):
        """
        animate sprite when hit
        """
        self.alpha += 50 * self.alpha_switch

        if not 0 <= self.alpha <= 255:
            self.alpha_switch *= -1
            self.animation_counter += 1
            self.alpha += 100 * self.alpha_switch

            if self.animation_counter == 6:
                self.__recover()
            self.image.set_alpha(self.alpha)

    def __recover(self):
        """
        reset after being damaged
        """
        self.damaged = False
        self.animation_counter = 1
        self.alpha = 255
        self.movement_speed *= 2

    def create_laser(self, direction: int, pos_y: int):
        """
        create lasers and add it to the group
        """
        laser: Laser = Laser(direction)

        left_wing_position: int = self.rect.x + 13
        right_wing_position: int = self.rect.x + (self.rect.width - 18)

        if self.side_switch:
            laser.set_position(left_wing_position, pos_y)
            self.side_switch = False
        else:
            laser.set_position(right_wing_position, pos_y)
            self.side_switch = True

        self.lasers.add(laser)

    def take_damage(self, value):
        """
        Reduce player health and set bool
        """
        self.__recover()
        self.health -= value
        self.damaged = True
        self.movement_speed /= 2

    def set_position(self, x: float, y: float):
        """set player positions"""
        self.x, self.y = x, y
        self.rect.x, self.rect.y = int(self.x), int(self.y)

    def update(self):
        """check for player updates"""
        if self.damaged:
            self.__animate()
