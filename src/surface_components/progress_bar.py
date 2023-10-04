from traceback import print_stack
from pygame import Surface, SRCALPHA, Rect


class ProgressBar:
    """Base class for a dynamic bar ui element"""

    image: Surface = None
    rect: Rect = None
    base_color: tuple = None
    color: tuple = None
    size: tuple = None

    __percentage: float = 1.0
    __get_percentage_cb: callable = None

    def __init__(
        self,
        position: tuple | list,
        size: tuple | list,
        color: tuple | list,
        percentage_cb: callable,
    ) -> None:
        """Progress bar component meant to be displayed on pygame Surfaces

        Args:
            size (tuple | list): total size
            color (tuple | list): _description_
            percentage_cb (callable): _description_
        """
        self.set_percentage_cb(percentage_cb)
        self.size = size
        self.image = Surface(size, flags=SRCALPHA)
        self.image.fill((10, 10, 10, 200))

        self.color = color
        self.base_color: tuple = (10, 10, 10, 200)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]

    def set_percentage_cb(self, percentage_cb: callable) -> None:
        """Set the call back function that returns a value from [0.0, 1.0]
        that represents the peercentage of the bar that should be displayed

        Args:
            percentage_cb (callable): callable function that returns a float value in range(0.0, 1.0)

        Raises:
            Exception: Invalid argument
            Exception: Invalid return type from callable argument

        Returns:
            None
        """
        if not callable(percentage_cb):
            print_stack()
            raise Exception(f"Invalid argument: {percentage_cb}\nExpected callable.")
        self.__get_percentage_cb = percentage_cb
        try:
            self.__percentage = float(self.__get_percentage_cb())
        except:
            print_stack()
            raise Exception(
                f"Invalid callable: {percentage_cb}\nExpected return value of type float."
            )

    def update(self) -> None:
        """Take the players current health percentage
        to the nearest whole number
        """
        self.__percentage = self.__get_percentage_cb()
        _img = Surface(
            ((self.size[0] * self.__percentage), self.rect.height - 10)
        ).convert()
        _img.fill(self.color)

        self.image.fill(self.base_color)
        self.image.blit(
            _img,
            (
                self.rect.x,
                self.rect.y,
            ),
        )
