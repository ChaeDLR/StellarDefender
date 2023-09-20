from ctypes import Structure
from pygame import Surface, Rect, font


class TextSurface(Structure):
    image: Surface = None
    rect: Rect = None

    __text_color = (120, 174, 90, 255)
    __text_font = None

    def __init__(self, txt: str, font_size: int) -> None:
        self.__text_font = font.SysFont(None, font_size, bold=True)
        self.image, self.rect = self.create_text((10, 10), "Score")

    def create_text(
        self,
        x_y: tuple,
        txt: str,
    ) -> tuple[Surface, Rect]:
        """
        x_y: tuple -> positions using center of the rect
        Tuple -> (text_img, text_rect)
        """
        text_img = self.__text_font.render(txt, 1, self.__text_color)
        text_rect = text_img.get_rect()
        text_rect.center = x_y
        return (text_img, text_rect)

    def update_text(self, new_text: str) -> None:
        self.image = self.__text_font.render(new_text, 1, self.__text_color)
        _pos = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = _pos
