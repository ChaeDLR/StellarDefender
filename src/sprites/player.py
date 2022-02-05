from typing import Literal, Union
from pygame import time
from dataclasses import field, make_dataclass


from ..base import ShipBase
from ..assets import Assets
from .laser import Laser


class Player(ShipBase):

    colors: tuple = None

    # movement flags
    flags = make_dataclass(
        "Flags",
        [
            ("FIRE", int, field(default=0)),
            ("MOVERIGHT", int, field(default=1)),
            ("MOVELEFT", int, field(default=2)),
            ("RECOIL", int, field(default=3)),
        ],
        frozen=True,
    )
    __active_flags: list[int] = []

    def __init__(self) -> None:
        super().__init__(Assets.get_image("player"), 6)
        self.base_speed: float = 10.0
        self.movement_speed: float = 10.0
        self.firing: bool = False
        self.__fire_cd: int = 250  # in milliseconds
        self.__prev_ticks: int = time.get_ticks()

        # flag callables
        self.__run_flag: dict[callable] = {
            self.flags.FIRE: self.create_laser,
            self.flags.MOVERIGHT: self.__move_right,
            self.flags.MOVELEFT: self.__move_left,
            self.flags.RECOIL: self.__recoil,
        }

        if not Player.colors:
            Player.colors = self._get_sprite_colors(self.image)

    def add_flag(self, flag: int) -> None:
        """Add a flag to the active flags list"""
        if flag in self.flags.__dict__.values() and flag not in self.__active_flags:
            self.__active_flags.append(flag)

    def remove_flag(self, flag: Union[int, list[int]]) -> None:
        """remove a flag from the active flags list"""
        try:
            for f in flag:
                self.__active_flags.remove(f)
        except:
            self.__active_flags.remove(flag)

    def __recoil(self, dir: Literal[1, -1] = 1) -> None:
        """React to a force"""
        # TODO: add player recoil when they try to go off the screen
        pass

    def __move_left(self) -> None:
        """move the player to the left"""
        if self.x - self.movement_speed <= 0:
            self.rect.x = 0
            self.x = float(self.rect.x)
        else:
            self.x -= self.movement_speed
            self.rect.x = int(self.x)

    def __move_right(self) -> None:
        """move the player to the right"""
        if (self.x + self.image.get_width() + self.movement_speed) > (
            self.screen_size[0]
        ):
            self.x = self.screen_size[0] - self.image.get_width()
            self.rect.x = int(self.x)

        else:
            self.x += self.movement_speed
            self.rect.x = int(self.x)

    def create_laser(self) -> None:
        if self.__fire_cd < (time.get_ticks() - self.__prev_ticks):
            super().create_laser(-1, (self.rect.top - Laser.w_h[1]))
            self.__prev_ticks = time.get_ticks()

    def update_particles(self) -> None:
        super().update_particles()
        self.lasers.update()

    def update(self, **kwargs) -> None:
        """update player movement and sprites"""
        for flag in self.__active_flags:
            self.__run_flag[flag]()

        super().update()

        if self.firing:
            self.create_laser()

        self.lasers.update()
