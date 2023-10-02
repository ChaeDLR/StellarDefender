from traceback import print_stack
from pygame import Surface, Rect, font


class TextSurface:
    image: Surface = None
    rect: Rect = None

    __text: str = ""
    __text_color: tuple = (120, 174, 90, 255)
    __text_font: font.Font = None
    __text_update_cb: callable = None

    def __init__(
        self, position: tuple | list, font_size: int, text_update_cb: callable
    ) -> None:
        self.__text_font = font.SysFont(None, font_size, bold=True)
        self.image, self.rect = self.__create_text((10, 10))
        self.rect.x, self.rect.y = position[0], position[1]

        if not callable(text_update_cb):
            print_stack()
            raise Exception(f"Invalid argument: {text_update_cb}\nExpected callable.")
        self.__text_update_cb = text_update_cb
        try:
            self.__text = str(self.__text_update_cb())
        except:
            print_stack()
            raise Exception(
                f"Invalid callable: {text_update_cb}\nExpected return value of type string."
            )

    def __create_text(self, x_y: tuple) -> tuple[Surface, Rect]:
        """
        x_y: tuple -> positions using center of the rect
        Tuple -> (text_img, text_rect)
        """
        text_img = self.__text_font.render(self.__text, 1, self.__text_color)
        text_rect = text_img.get_rect()
        text_rect.center = x_y
        return (text_img, text_rect)

    def set_text(self, txt: str) -> None:
        """Set the components text

        Args:
            txt (str): Text to be displayed on the image surface.

        Raises:
            Exception: cannot convert to string
        """
        try:
            self.__text = str(txt)
        except TypeError:
            print_stack()
            raise Exception(f"Invalid argument: {txt}\nExpected string.")

    def update(self) -> None:
        self.__text = self.__text_update_cb()
        self.image = self.__text_font.render(self.__text, 1, self.__text_color)
        _pos = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = _pos
