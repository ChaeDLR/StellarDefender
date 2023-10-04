from pygame import event, time, Vector2

from ..base import ShipBase
from ..assets import get_image
from .laser import SLaser


class Enemy(ShipBase):
    """basic enemy class"""

    colors: tuple = None
    size: tuple = (64, 64)

    __base_health: int = 4

    def __init__(self, attack_speed: int = 1000) -> None:
        """initialize sprite variables, get image, and create events"""
        self.basicatk_event = event.Event(
            event.custom_type(),
            {"speed": attack_speed, "capture": 0, "attack": self._create_laser},
        )
        self.specialatk_event = event.Event(
            event.custom_type(),
            {
                "speed": int(attack_speed * 2.25),
                "capture": 0,
                "attack": self._create_special_laser,
            },
        )

        super().__init__(
            get_image("enemy"),
            self.__base_health,
            [self.basicatk_event, self.specialatk_event],
        )

        if not Enemy.colors:
            Enemy.colors = self._get_sprite_colors(self.image)

    def _create_laser(self):
        """override"""
        super()._create_laser(Vector2(0, 1), self.rect.bottom)
        self.basic_attack()

    def _create_special_laser(self):
        """
        Create a special attack laser object and add it to a sprite group
        """
        s_laser: SLaser = SLaser(Vector2(0, 1))
        s_laser.set_position(self.rect.midbottom[0], self.rect.midbottom[1])
        self.lasers.add(s_laser)
        self.special_attack()

    def recover(self) -> None:
        """override"""
        self._recover(self.__base_health)

    def resume(self) -> None:
        """start attacks from captures"""
        time.set_timer(self.basicatk_event, self.basicatk_event.capture, 1)
        time.set_timer(self.specialatk_event, self.specialatk_event.capture, 1)

    def attack(self) -> None:
        """start enemy's attack timers"""
        self.basic_attack()
        self.special_attack()

    def basic_attack(self) -> None:
        """send attack events to the event queue on timers"""
        time.set_timer(self.basicatk_event, self.basicatk_event.speed, 1)
        self.basicatk_event.capture = time.get_ticks()

    def special_attack(self) -> None:
        time.set_timer(self.specialatk_event, self.specialatk_event.speed, 1)
        self.specialatk_event.capture = time.get_ticks()

    def capture_attack_timers(self) -> None:
        horas: int = time.get_ticks()

        self.basicatk_event.capture = self.basicatk_event.speed - (
            horas - self.basicatk_event.capture
        )
        if (
            self.basicatk_event.capture > self.basicatk_event.speed
            or self.basicatk_event.capture <= 1
        ):
            self.basicatk_event.capture = self.basicatk_event.speed

        self.specialatk_event.capture = self.specialatk_event.speed - (
            horas - self.specialatk_event.capture
        )
        if (
            self.specialatk_event.capture > self.specialatk_event.speed
            or self.specialatk_event.capture <= 1
        ):
            self.specialatk_event.capture = self.specialatk_event.speed

    def update_particles(self) -> None:
        """update particle effect"""
        super().update_particles()
        self.lasers.update()

    def update(self, x: int, y: int):
        """
        override - update enemy sprite
        """
        self.x += self._track(self.rect.centerx, x)
        self.rect.centerx = int(self.x)

        if y:
            self.y += self._track(self.rect.centery, y)
            self.rect.centery = int(self.y)

        self.lasers.update()
        super().update()
