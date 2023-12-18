from pygame import sprite, Surface, Vector2
from math import pi, sin, radians


class _Projectile(sprite.Sprite):
    """Projectile base class"""

    __color: tuple = (0, 0, 0)
    __explosion_colors: tuple = ((0, 0, 0), (255, 255, 255))

    def __init__(self, direction: Vector2, size: tuple = None):
        """
        dir(direction): int -> 1 (moving down), -1 (moving up)
        rect: tuple -> = (x, y, width, height)
        """
        if not isinstance(direction, Vector2):
            raise TypeError

        super().__init__()
        self.direction: Vector2 = direction

        if size:
            self.image: Surface = Surface(size)
            self.rect = self.image.get_rect()

    def get_color(self) -> tuple:
        return self.__color

    @classmethod
    def get_explosion_colors(self) -> tuple:
        return self.__explosion_colors

    def set_position(self, x: int, y: int):
        """set laser position using topleft"""
        self.rect.x, self.rect.y = x, y
        self.x, self.y = float(self.rect.x), float(self.rect.y)

    def get_position(self) -> tuple:
        return self.rect.center


class Laser(_Projectile):
    """projectile"""

    w_h: tuple = (3, 12)

    def __init__(self, direction: Vector2) -> None:
        """
        img: Surface -> laser.png
        """
        super().__init__(direction, self.w_h)
        self.damage: int = 1
        self.__color = (255, 100, 100)
        self.__explosion_colors = ((210, 90, 90), (10, 10, 10), (106, 104, 109))
        self.image.fill(self.__color)

    def update(self):
        """
        update laser pos
        """
        self.y += 15 * self.direction.y
        self.rect.y = int(self.y)

        self.x += 15 * self.direction.x
        self.rect.x = int(self.x)


class SLaser(_Projectile):
    """Special attack laser"""

    w_h: tuple = (8, 8)

    def __init__(self, direct: int) -> None:
        super().__init__(direct, self.w_h)
        self.__color = (150, 150, 230)
        self.image.fill(self.__color)
        self.image.convert_alpha()

        self.alpha: int = 255
        self.alpha_switch: int = 1

        self.damage: int = 2

    def update(self):
        """
        move the laser, dir: int -> 1 (moving down), -1 (moving up)
        """
        self.y += 4 * self.direction.y
        self.x += 18 * sin(((2 * pi * 0.008) * self.y) + radians(self.y))

        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

        # Make the projectile blink
        self.alpha -= 15 * self.alpha_switch
        if not 100 <= self.alpha <= 255:
            self.alpha_switch *= -1
            self.alpha -= 30 * self.alpha_switch
        self.image.set_alpha(self.alpha)
