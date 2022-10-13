from pygame import sprite, Surface
from math import pi, sin, radians


class _Projectile(sprite.Sprite):
    """Projectile base class"""

    def __init__(self, direct: int, size: tuple = None):
        """
        dir(direction): int -> 1 (moving down), -1 (moving up)
        rect: tuple -> = (x, y, width, height)
        """
        super().__init__()
        self.direction: int = direct
        if size:
            self.image: Surface = Surface(size)
            self.rect = self.image.get_rect()

    def set_position(self, x: int, y: int):
        """set laser position using topleft"""
        self.rect.x, self.rect.y = x, y
        self.x, self.y = float(self.rect.x), float(self.rect.y)


class Laser(_Projectile):
    """projectile"""

    w_h: tuple = (3, 12)

    def __init__(self, direct: int) -> None:
        """
        img: Surface -> laser.png
        """
        super().__init__(direct, self.w_h)
        self.image.fill((255, 100, 100))

        self.damage: int = 1

    def update(self):
        """
        update laser pos
        """
        self.y += 15 * self.direction
        self.rect.y = int(self.y)


class SLaser(_Projectile):
    """Special attack laser"""

    w_h: tuple = (8, 8)

    def __init__(self, direct: int) -> None:
        super().__init__(direct, self.w_h)
        self.image.fill((150, 150, 230))
        self.image.convert_alpha()

        self.alpha: int = 255
        self.alpha_switch: int = 1

        self.damage: int = 2

    def update(self):
        """
        move the laser, dir: int -> 1 (moving down), -1 (moving up)
        """
        self.y += 4 * self.direction
        self.x += 18 * sin(((2 * pi * 0.008) * self.y) + radians(self.y))

        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

        # Make the projectile blink
        self.alpha -= 15 * self.alpha_switch
        if not 100 <= self.alpha <= 255:
            self.alpha_switch *= -1
            self.alpha -= 30 * self.alpha_switch
        self.image.set_alpha(self.alpha)
