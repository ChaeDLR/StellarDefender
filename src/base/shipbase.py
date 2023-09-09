from math import cos, sin, atan2, degrees, pi

from pygame import Surface, sprite, surfarray
from pygame import event, Vector2, time, mask
from pygame.transform import rotate

from ..settings import size
from ..sprites import Laser


class ShipBase(sprite.Sprite):
    """
    A base class for all of the ship sprites
    """

    health: int = 1
    base_speed: float = 5.5
    movement_speed: float = 5.5
    alpha: int = 255
    alpha_switch: int = 1
    alpha_counter: int = 1

    side_switch: bool = True
    damaged: bool = False
    dying: bool = False

    def __init__(self, image_: Surface, health_: int, events_: list[event.Event] = []):
        super().__init__()
        self.screen_size = size
        self.health = health_
        self.events: list[event.Event] = events_
        self.image: Surface = image_
        self.rect = self.image.get_rect()
        self.x, self.y = float(self.rect.centerx), float(self.rect.centery)
        self.center = self.rect.center
        self.lasers = sprite.Group()

    def __generate_particles(self) -> list:
        """
        Use class's colors var and generate a list of particles
        """
        particles: list = []
        for n, color in enumerate(self.colors):
            particles.append(
                _Particle(
                    color=color,
                    radius=(self.rect.w / 4) - n,
                    velocity=1.9 * (n + 1),
                    offset=(n, n),
                    center=self.rect.center,
                )
            )
        return particles

    def __animate(self) -> None:
        """
        slow movement and osc alpha when hit
        """
        self.alpha += 50 * self.alpha_switch

        if not 0 <= self.alpha <= 255:
            self.alpha_switch *= -1
            self.alpha_counter += 1
            self.alpha += 100 * self.alpha_switch

            if self.alpha_counter == 6:
                self._recover()
            self.image.set_alpha(self.alpha)

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
        start ---> dest
        increase speed variable to track slower
        decrease to track faster
        """
        return (dest - start) / speed

    def _recover(self, health_: int = 0) -> None:
        """
        reset after being damaged
        """
        self.dying = False
        self.damaged = False
        self.alpha_counter = 1
        self.alpha = 255
        self.movement_speed = self.base_speed * (
            self.movement_speed / abs(self.movement_speed)
        )
        self.image.set_alpha(self.alpha)
        if health_ > 0:
            self.health = health_

    def _create_laser(self, direction: Vector2, pos_y: int, rotate_toward: list | tuple=None) -> None:
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

        if rotate_toward:
            try:
                dx = rotate_toward[0] - laser.x
                dy = rotate_toward[1]- laser.y
            except TypeError as ex:
                raise ex
            radians = atan2(-dy, dx)
            radians %= 2 * pi
            rotation = degrees(radians) + 90

            laser.image = rotate(laser.image, rotation)
            laser.rect = laser.image.get_rect(center=laser.rect.center)
            laser.mask = mask.from_surface(laser.image)

        self.lasers.add(laser)


    def take_damage(self, value) -> None:
        """
        Reduce player health and set bool
        """
        if not self.dying:
            self.health -= value
            if self.health <= 0:
                self.dying = True
                self.color_particles = self.__generate_particles()
                for event_ in self.events:
                    time.set_timer(event_, 0)
                    event.clear(event_.type)
            else:
                self.damaged = True
                self.movement_speed /= 2

    def set_position(self, x: float, y: float) -> None:
        """set player positions"""
        self.x, self.y = x, y
        self.rect.centerx, self.rect.centery = int(self.x), int(self.y)
        self.center = self.rect.center

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
        self.angle: float = 0.0

        self.__angle_velocity: float = 1 / self.radius

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
            self.positions[i].x += int(
                (self.velocity * self.directions[i][0]) * cos(self.angle)
            )

            self.positions[i].y += int(
                (self.velocity * self.directions[i][1]) * sin(self.angle)
            )

        if 15.0 < self.alpha <= 255.0:
            self.alpha -= self.velocity
        else:
            self.alpha = 0.0

        self.color[3] = int(self.alpha)
        self.radius -= 0.2
        self.angle += self.__angle_velocity
