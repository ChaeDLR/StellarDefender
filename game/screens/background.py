import random

from pygame import SRCALPHA, Surface, draw, Vector2


class Background:
    """Scrolling space background"""

    screen_dims: tuple = None

    def __init__(self, w_h: tuple):
        """
        w_h: tuple -> (screen_width, screen_height)
        """
        # create all of the background's basic variables
        # set size of the background
        Background.screen_dims: tuple = w_h
        # set color to black
        self.color: tuple = (1, 1, 1)
        # create the image and pass SRCALPHA so that the image will display (R, G, B, A) and not only (R, G, B)
        self.image = Surface(self.screen_dims, flags=SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        # Iterator to hold all of the background's generated stars
        self.starbatch: list = []
        # create the stars and populate the starbatch list
        self.__create_starbatch()

    def __create_starbatch(self):
        """
        Create a batch of stars
        circles of the color yellow with random variables
        that will control the behavior
        """
        for _ in range(0, 10):
            new_star = _Star()
            self.starbatch.append(new_star)

    def update(self):
        """
        scroll stars and generate new ones
        """
        self.image.fill(self.color)
        for star in self.starbatch:
            draw.circle(
                self.image,
                star.color,
                star.center,
                star.radius,
            )
            star.update()
            if star.center.y > Background.screen_dims[1]:
                star.reset()


class _Star:
    """class to generate a star"""

    def __init__(self):
        random.seed()

        # generate color of the star with a random alpha value
        self.color: list = [255, 255, 175, random.randint(60, 100)]
        # generate position
        self.center = Vector2(
            float(random.randint(0, Background.screen_dims[0])),
            float(random.randint(0, Background.screen_dims[1])),
        )
        # generate circle size
        self.radius: int = random.randint(1, 3)
        # choose the movementspeed based on the star size
        self.movement_speed: float = self.radius
        # create the bounds the star's alpha should stay within
        self.alpha_limits: tuple = (self.color[3] - 51, self.color[3] + 50)
        # create value the alpha will be increased by
        self.alpha_inc: int = 2
        # create speed value that the star should blink at
        self.blink_speed: int = random.randint(10, 35)
        self.blink_counter: int = 1

    def reset(self):
        """
        Reset the star's positions to the top of the screen and generate a new x
        """
        self.center = Vector2(
            float(random.randint(0, Background.screen_dims[0])),
            0,
        )

    def update(self):
        """
        update stars values
        """
        if (
            self.alpha_limits[0] >= self.color[3]
            or self.alpha_limits[1] <= self.color[3]
        ):
            self.alpha_inc *= -1

        if self.blink_speed % self.blink_counter == 0:
            self.color[3] += self.alpha_inc
            self.blink_counter = 1
        else:
            self.blink_counter += 1

        self.center.y += self.movement_speed
