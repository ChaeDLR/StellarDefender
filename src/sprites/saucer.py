import random

from pygame import event, time
from typing import Literal

from ..assets import Assets
from .ship import Ship
from ..settings import width


class Saucer(Ship):

    colors: tuple = None
    size: tuple = (96, 64)

    __attack_speed: int = 2500
    __animation_index: int = 0

    def __init__(self) -> None:
        """Saucer enemy class"""
        self.images: dict = Assets.get_image("saucer")
        # Image keys
        # "charge" -> "0", "1", "2"
        # "idle" -> "0"
        self.current_animation: Literal["idle", "charge"] = "idle"

        self.atk_event = event.Event(
            event.custom_type(),
            {
                "speed": self.attack_speed,
                "capture": 0,
                "attack": self.create_blast
            }
        )

        super().__init__(
                self.images[self.current_animation][0],
                7,
                [self.atk_event]
            )

        self.movement_speed: float = 3.5

        # sets the pace of the animation
        self.animation_counter: int = 0

        self.xbounds: tuple = (
            int(self.rect.width / 2),
            int(width - (self.rect.width / 2)),
        )

        if not Saucer.colors:
            Saucer.colors = self._get_sprite_colors(self.image)

        random.seed()

    @property
    def animation_index(self) -> int:
        """return the current animation index if it is within range"""
        if not self.__animation_index < len(self.images[self.current_animation]):
            self.__animation_index = 0
        return self.__animation_index

    @property
    def attack_speed(self) -> int:
        """return an random attack speed within a range"""
        return self.__attack_speed + (self.__attack_speed * random.random())

    def recover(self) -> None:
        """override"""
        self._recover()

    def attack(self) -> None:
        """start attack timners"""
        pass

    def resume(self) -> None:
        """resume attacks, start timers from capture"""
        pass

    def capture_attack_timers(self) -> None:
        pass

    def cancel_timers(self):
        """Stop all of the class's timers"""
        pass

    def create_blast(self) -> None:
        """Create saucers blast attack and add it to a sprite group"""
        pass

    def update(self, x: int, y: int):
        """update the saucer's position"""

        if not self.xbounds[0] <= self.rect.centerx <= self.xbounds[1]:
            self.movement_speed *= -1
        self.x += self.movement_speed
        self.rect.x = int(self.x)

        if y:
            self.y += self._track(self.rect.centery, y)
            self.rect.centery = int(self.y)

        super().update()
