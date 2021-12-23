from pygame import event, time
from game import Assets

from .ship import Ship
from ..settings import width


class Saucer(Ship):

    colors: tuple = None
    size: tuple = (96, 64)

    def __init__(self) -> None:
        """Saucer enemy class"""
        images = Assets.get_image("saucer")
        print("=======================================")
        # TODO: FIX KEYS
        # Keys are currently the entire  path to the image
        for key in images:
            print(f"Imgs key: {key}\nKey's value = {images[key]}\n")
        # Image keys
        # "charge" -> "0", "1", "2"
        # "fire" -> "0", "1"
        # "idle" -> "0"
        # super.__init__(images["idle"])

        self.xbounds: tuple = (
            int(self.rect.width / 2),
            int(width - (self.rect.width / 2)),
        )

    def update(self, *args, y: int):
        """update the saucer's position"""

        if not (self.xbounds[0] < self.rect.centerx < self.xbounds[1]):
            self.movement_speed *= -1
        self.x += self.movement_speed

        self.y += self._track(self.rect.centery, y)
        self.rect.centery = int(self.y)

        super().update()
