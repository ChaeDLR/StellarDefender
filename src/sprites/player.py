from typing import Literal
from pygame import time
from math import log
from dataclasses import dataclass, field, make_dataclass

from ..base import ShipBase
from ..assets import Assets
from .laser import Laser


class Player(ShipBase):

    colors: tuple = None

    # movement flags
    flags = make_dataclass(
        "Flags",
        [
            (
                "Fire",
                dataclass,
                make_dataclass(
                    "Fire",
                    [
                        ("KEY", int, field(default=0)),
                        ("priority", int, field(default=2)),
                    ],
                    frozen=True,
                ),
            ),
            (
                "MoveRight",
                dataclass,
                make_dataclass(
                    "MoveRight",
                    [
                        ("KEY", int, field(default=1)),
                        ("priority", int, field(default=2)),
                    ],
                    frozen=True,
                ),
            ),
            (
                "MoveLeft",
                dataclass,
                make_dataclass(
                    "MoveLeft",
                    [
                        ("KEY", int, field(default=2)),
                        ("priority", int, field(default=2)),
                    ],
                    frozen=True,
                ),
            ),
            (
                "Recoil",
                dataclass,
                make_dataclass(
                    "Recoil",
                    [
                        ("KEY", int, field(default=3)),
                        ("priority", int, field(default=1)),
                    ],
                    frozen=True,
                ),
            ),
        ],
        frozen=True,
    )

    # active flags separated into lists by priority.
    __active_flags: dict[list[int]] = {1: [], 2: []}  # priority flags
    __fire_cd: int = 250  # in milliseconds
    __direction: Literal[1, -1] = 1  # 1 = right, -1 = left. across x-axis

    def __init__(self) -> None:
        super().__init__(Assets.get_image("player"), 6)
        self.base_speed: float = 10.0
        self.movement_speed: float = 10.0
        self.firing: bool = False
        # flag callables
        self.__run_flag: dict[callable] = {
            self.flags.Fire.KEY: self.create_laser,
            self.flags.MoveRight.KEY: self.__move_right,
            self.flags.MoveLeft.KEY: self.__move_left,
            self.flags.Recoil.KEY: self.__recoil,
        }

        if not Player.colors:
            Player.colors = self._get_sprite_colors(self.image)

        row_wdth: int = int(self.screen_size[0] / 24)
        self.__recoil_bounds: tuple = (
            row_wdth,
            int(self.screen_size[0] - row_wdth),
        )
        self.__prev_ticks: int = time.get_ticks()

    @property
    def direction(self) -> int:
        """get the x direction modifier. Only used for Priority 1 flags."""
        return self.__direction

    @direction.setter
    def direction(self, dir: Literal[1, -1]) -> None:
        """Set the direction to left(-1) or right(1)"""
        if dir not in [1, -1]:
            raise ValueError
        self.__direction = dir

    def add_flag(self, flag: dataclass) -> None:
        """Add a flag to the active flags list"""
        if (
            flag in self.flags.__dict__.values()
            and flag not in self.__active_flags[flag.priority]
        ):
            self.__active_flags[flag.priority].append(flag)

    def remove_flag(self, flag: dataclass) -> None:
        """remove a flag from the active flags list"""
        self.__active_flags[flag.priority].remove(flag)

    def __recoil(self) -> None:
        """React to a force"""
        self.x += (
            log(self.movement_speed + (self.movement_speed * self.x), 2)
            * self.direction
        )

        if (self.direction > 0 and self.x > self.__recoil_bounds[0]) or (
            self.direction < 0 and self.x < self.__recoil_bounds[1]
        ):
            self.remove_flag(self.flags.Recoil)
        else:
            self.rect.centerx = int(self.x)

    def __move_left(self) -> None:
        """move the player to the left"""
        if self.x - self.movement_speed <= 0:
            self.rect.centerx = 0
            self.x = 0.0
            # start recoil
            self.add_flag(self.flags.Recoil)
            self.direction = 1
        else:
            self.x -= self.movement_speed
            self.rect.centerx = int(self.x)

    def __move_right(self) -> None:
        """move the player to the right"""
        if (self.x + self.movement_speed) > self.screen_size[0]:
            self.x = self.screen_size[0] - self.image.get_width()
            self.rect.centerx = int(self.x)
            # start recoil
            self.add_flag(self.flags.Recoil)
            self.direction = -1
        else:
            self.x += self.movement_speed
            self.rect.centerx = int(self.x)

    def create_laser(self) -> None:
        if self.__fire_cd < (time.get_ticks() - self.__prev_ticks):
            super().create_laser(-1, (self.rect.top - Laser.w_h[1]))
            self.__prev_ticks = time.get_ticks()

    def update_particles(self) -> None:
        super().update_particles()
        self.lasers.update()

    def update(self, **kwargs) -> None:
        """update player movement and sprites"""

        # use priority 1 list if there are active flags in it
        priority: int = 1 if self.__active_flags[1] else 2

        for flag in self.__active_flags[priority]:
            self.__run_flag[flag.KEY]()

        super().update()

        if self.firing:
            self.create_laser()

        self.lasers.update()
