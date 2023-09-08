import random

from pygame import event, time
from typing import Literal

from ..base import ShipBase
from ..settings import width
from ..assets import get_image


class Saucer(ShipBase):
    colors: tuple = None
    size: tuple = (96, 64)

    __base_health: int = 7
    __attack_speed: int = 2500
    __animation_index: int = 0

    def __init__(self) -> None:
        """Saucer enemy class"""
        self.images: dict = get_image("saucer")
        # Image keys
        # "charge" -> "0", "1", "2"
        # "idle" -> "0"
        self.current_animation: Literal["idle", "charge"] = "idle"

        self.atk_event = event.Event(
            event.custom_type(),
            {"speed": self.attack_speed, "capture": 0, "attack": self._create_laser},
        )

        super().__init__(
            self.images[self.current_animation][0], self.__base_health, [self.atk_event]
        )

        self.base_speed: float = 3.5
        self.movement_speed: float = self.base_speed

        # sets the pace of the animation
        self.animation_counter: int = 0

        self.xbounds: tuple = (
            int(self.rect.width / 2),
            int(width - (self.rect.width / 2)),
        )

        if not Saucer.colors:
            Saucer.colors = self._get_sprite_colors(self.image)

        random.seed()

    def _create_laser(self) -> None:
        """saucer attack"""
        super()._create_laser(1, self.rect.centery)
        self.attack()

    @property
    def animation_index(self) -> int:
        """return the current animation index if it is within range"""
        if not self.__animation_index < len(self.images[self.current_animation]):
            self.__animation_index = 0
        return self.__animation_index

    @property
    def attack_speed(self) -> int:
        """return an random attack speed within a range"""
        return self.__attack_speed + int((self.__attack_speed * random.random()))

    def recover(self) -> None:
        """override"""
        self._recover(self.__base_health)

    def attack(self, resume: bool = False) -> None:
        """start attack timners"""
        if resume:
            time.set_timer(self.atk_event, self.atk_event.capture, 1)
        else:
            time.set_timer(self.atk_event, self.atk_event.speed, 1)
        self.atk_event.capture = time.get_ticks()

    def resume(self) -> None:
        """resume attacks, start timers from capture"""
        self.attack(True)

    def capture_attack_timers(self) -> None:
        """capture the current progress of the timers"""
        self.atk_event.capture = self.atk_event.speed - (
            time.get_ticks() - self.atk_event.capture
        )
        if self.atk_event.capture > self.atk_event.speed or self.atk_event.capture <= 1:
            self.atk_event.capture = self.atk_event.speed

    def cancel_timers(self):
        """Stop all of the class's timers"""
        pass

    def update(self, x: int, y: int):
        """update the saucer's position"""
        super().update()
        if not self.xbounds[0] <= self.rect.centerx <= self.xbounds[1]:
            self.movement_speed *= -1
        self.x += self.movement_speed
        self.rect.x = int(self.x)

        if y:
            self.y += self._track(self.rect.centery, y)
            self.rect.centery = int(self.y)

        self.lasers.update()
