from pygame import Surface, SRCALPHA, Rect, Vector2


class ProgressBar:
    """Base class for a dynamic bar ui element"""

    image: Surface = None
    rect: Rect = None
    base_color: tuple = None
    color: tuple = None
    size: tuple = None

    def __init__(
        self,
        coords: tuple | list = None,
        size: tuple | list = None,
        color: tuple | list = None,
    ) -> None:
        self.size = size
        self.image = Surface(size, flags=SRCALPHA)
        self.image.fill((10, 10, 10, 200))

        self.color = color
        self.base_color: tuple = (10, 10, 10, 200)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords

    def update(self, percentage: float):
        """
        Take the players current health percentage
        to the nearest whole number
        """
        _img = Surface(
            ((self.size[0] * percentage) - 20, self.rect.height - 10)
        ).convert()
        _img.fill(self.color)

        self.image.fill(self.base_color)
        self.image.blit(
            _img,
            (
                self.rect.x,
                self.rect.y - 5,
            ),
        )
