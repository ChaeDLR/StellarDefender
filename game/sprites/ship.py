from pygame import Surface, sprite, surfarray
from pygame import event, Vector2, time

from typing import Union

import pygame

from ..settings import screen_dims
from .laser import Laser


class Ship(sprite.Sprite):
    """
    A base class for all of the ship sprites
    """

    base_speed: float = 5.5
    movement_speed: float = 5.5
    alpha: int = 255
    alpha_switch: int = 1
    animation_counter: int = 1

    moving_left, moving_right = False, False
    side_switch: bool = True
    damaged: bool = False
    dying: bool = False

    # hold the sprites custom events
    _timers: list[event.Event] = []

    def __init__(self, img: Surface):
        super().__init__()
        self.screen_dims = screen_dims

        self.image: Surface = img
        self.colors: tuple = self._get_sprite_colors(self.image)
        self.rect = self.image.get_rect()
        self.x, self.y = float(self.rect.centerx), float(self.rect.centery)

        self.image.set_alpha(self.alpha)

        self.lasers = sprite.Group()

    def __del__(self):
        """sprite finalizer"""
        try:
            for timer in self._timers:
                time.set_timer(timer, 0)
            event.get(self.timer_types)
        except:
            print(f"Timer: {timer}, failed.")

    def _get_sprite_colors(self, img: Surface) -> tuple:
        """
        Loop through a surface and grab the colors its made of
        sort from lightest(n) to darkest(0)
        """
        colors: list = []
        for row in surfarray.array3d(img):
            for pixel in row:
                rgb: list = [int(pixel[0]), int(pixel[1]), int(pixel[2]), 255]
                if rgb not in [[255, 255, 255, 255], [0, 0, 0, 255]] + colors:
                    colors.append(rgb)
        colors.sort(key=sum)
        return tuple(colors)

    def _track(self, start: int, dest: int, speed: int = 40) -> float:
        """
        calculate a gradual movement from
        start ----> dest
        increase speed variable to track slower
        decrease to track faster
        """
        return (dest - start) / speed

    def __generate_particles(self) -> list:
        """
        Take a list of colors and generate a list of particles
        """
        particles: list = []
        for n, color in enumerate(self.colors):
            particles.append(
                _Particle(
                    color=color,
                    radius=(self.rect.w / 4) - n,
                    velocity=0.8 * (n + 1),
                    offset=(n, n),
                    center=self.rect.center,
                )
            )
        return particles

    def __animate(self) -> None:
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

    def __recover(self) -> None:
        """
        reset after being damaged
        """
        self.damaged = False
        self.animation_counter = 1
        self.alpha = 255
        self.movement_speed = self.base_speed

    @property
    def timer_types(self) -> list:
        return [timer.type for timer in self._timers]

    @property
    def timers(self) -> list:
        return self._timers

    def add_timer(self, timer: Union[event.Event, list[event.Event]]) -> None:
        """add a single timer or a list of timers"""
        if isinstance(timer, list):
            for new_timer in timer:
                if hasattr(new_timer, "sprite"):
                    self._timers.append(new_timer)
        elif isinstance(timer, event.Event) and hasattr(event, "sprite"):
            self._timers.append(timer)
        else:
            print(f"Timer: {timer} is invalid.")
            raise

    def start_timers(self) -> None:
        """start all of the class's timers"""
        for timer in self._timers:
            time.set_timer(timer, timer.speed)

    def cancel_timers(self) -> None:
        for timer in self._timers:
            time.set_timer(timer, 0)

    def pause_timers(self) -> None:
        """cancel all of the timers and capture their progress rate"""
        ticks = time.get_ticks()
        for timer in self._timers:
            cap: int = ticks - timer.capture

            if cap >= timer.speed:
                cap = timer.speed

            timer.capture = cap
            time.set_timer(timer, 0)
            pygame.event.clear(timer.type)
            print("clearing timers")

    def unpause_timers(self) -> None:
        """resume paused timers and restart their loops"""
        for timer in self._timers:
            time.set_timer(timer, timer.capture, 1)
            time.set_timer(timer.vivify, timer.capture, 1)

    def create_laser(self, direction: int, pos_y: int) -> None:
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

    def take_damage(self, value) -> None:
        """
        Reduce player health and set bool
        """
        if not self.dying:
            self.__recover()
            self.health -= value
            if self.health <= 0:
                self.dying = True
                self.color_particles = self.__generate_particles()
            else:
                self.damaged = True
                self.movement_speed /= 2

    def set_position(self, x: float, y: float) -> None:
        """set player positions"""
        self.x, self.y = x, y
        self.rect.centerx, self.rect.centery = int(self.x), int(self.y)

    def update_particles(self) -> None:
        for particle in self.color_particles:
            particle.update()

    def update(self) -> None:
        """Update damaged animation if ship is damaged"""
        if self.damaged:
            self.__animate()


class _Particle:

    directions: tuple = (
        # left
        (-1, 0),
        # right
        (1, 0),
        # up
        (0, -1),
        # down
        (0, 1),
        # top left
        (-1, -1),
        # bottom left
        (-1, 1),
        # top right
        (1, -1),
        # bottom right
        (1, 1),
    )

    def __init__(
        self,
        color: tuple,
        radius: int,
        velocity: float,
        offset: tuple,
        center: tuple[int, int],
    ):

        self.color: list = list(color)
        self.radius: int = radius
        self.velocity: float = velocity
        self.offset: tuple = offset
        self.alpha: float = 255.0

        self.positions: list = [Vector2((0, 0)) for _ in self.directions]
        for i, position in enumerate(self.positions):
            position.x = int(center[0] + (self.offset[0] * self.directions[i][0]))
            position.y = int(center[1] + (self.offset[1] * self.directions[i][1]))

    def update(self):
        """
        Move the particle
        Lower the alpha
        Lower the radius
        """
        for i in range(len(self.positions)):
            self.positions[i].x += int(self.velocity * self.directions[i][0])
            self.positions[i].y += int(self.velocity * self.directions[i][1])

        if 15.0 < self.alpha <= 255.0:
            self.alpha -= self.velocity
        else:
            self.alpha = 0.0

        self.color[3] = int(self.alpha)
        self.radius -= 0.2
