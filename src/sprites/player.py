import pygame
import math

from typing import Literal
from math import log
from dataclasses import dataclass, field, make_dataclass

from ..base import ShipBase
from ..assets import get_image
from .laser import Laser


class Player(ShipBase):
    colors: tuple = None

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

    __fire_cd: int = 250  # in milliseconds
    __direction: Literal[1, -1] = 1  # 1 = right, -1 = left. across x-axis

    # region properties

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

    # endregion

    def __init__(self) -> None:
        super().__init__(get_image("player"), 10)
        self.base_speed: float = 10.0
        self.movement_speed: float = 10.0
        self.osc_speed: int = 1.7
        self.osc_bounds = (self.rect.y, self.rect.y)
        self.firing: bool = False
        # active flags separated into lists by priority.
        # 1 = top priority, loss of control
        # 2 = 2nd priority, player controlled
        self.__active_flags: dict[list[int]] = {1: [], 2: []}
        # flag callables
        self.__run_flag: dict[callable] = {
            self.flags.Fire.KEY: self._create_laser,
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
        self.__prev_ticks: int = pygame.time.get_ticks()

    # region private methods

    def __recoil(self) -> None:
        """horizontal bounce"""
        self.x += (
            log(self.movement_speed + (self.movement_speed * self.x), 2)
            * self.direction
        ) * 2

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

    def _create_laser(self) -> None:
        if self.__fire_cd < (pygame.time.get_ticks() - self.__prev_ticks):
            mpos = pygame.mouse.get_pos()
            radians = math.atan2(self.y - mpos[1], self.x - mpos[0])
            _dir = pygame.Vector2(math.cos(radians) * -1, math.sin(radians) * -1)

            super()._create_laser(_dir, (self.rect.top - Laser.w_h[1]), mpos)
            self.__prev_ticks = pygame.time.get_ticks()

    # endregion

    # region public methods

    def set_position(self, x: float, y: float) -> None:
        super().set_position(x, y)
        self.osc_bounds = (self.rect.y + 14, self.rect.y - 20)

    def add_flag(self, flag: dataclass) -> None:
        """Add a flag to the active flags list"""
        if (
            flag in self.flags.__dict__.values()
            and flag not in self.__active_flags[flag.priority]
        ):
            self.__active_flags[flag.priority].append(flag)

    def remove_flag(self, flag: dataclass) -> None:
        """remove a flag from the active flags list"""
        try:
            self.__active_flags[flag.priority].remove(flag)
        except:
            # todo: add logging
            pass

    def keydown_handler(self, event: pygame.event.Event) -> None:
        """respond to users keyboard inputs"""
        if event.key == pygame.K_SPACE and self.health > 0:
            self.add_flag(self.flags.Fire)

        elif event.key == pygame.K_a:
            self.add_flag(self.flags.MoveLeft)

        elif event.key == pygame.K_d:
            self.add_flag(self.flags.MoveRight)

    def keyup_handler(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_SPACE:
            self.remove_flag(self.flags.Fire)

        elif event.key == pygame.K_a:
            self.remove_flag(self.flags.MoveLeft)

        elif event.key == pygame.K_d:
            self.remove_flag(self.flags.MoveRight)

    def mousedown_handler(self, event: pygame.event.Event) -> None:
        if event.button == pygame.BUTTON_LEFT and self.health > 0:
            self.add_flag(self.flags.Fire)

    def mouseup_handler(self, event: pygame.event.Event) -> None:
        if event.button == pygame.BUTTON_LEFT:
            self.remove_flag(self.flags.Fire)

    def update_particles(self) -> None:
        super().update_particles()
        self.lasers.update()

    def update(self, **kwargs) -> None:
        """update player movement and sprites"""

        # use priority 1 list if there are active flags in it
        priority: int = 1 if self.__active_flags[1] else 2

        for flag in self.__active_flags[priority]:
            self.__run_flag[flag.KEY]()

        # osc player vertically
        if self.health > 1:
            if not self.osc_bounds[1] <= self.y <= self.osc_bounds[0]:
                self.osc_speed *= -1
                self.y += self.osc_speed
            self.y += self.osc_speed
            self.rect.y = self.y

        super().update()

        if self.firing:
            self._create_laser()

        self.lasers.update()

    # endregion
