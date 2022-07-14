import traceback

from pygame import Surface, Rect, font
from typing import Sequence, Tuple, Union

from .screenbase import ScreenBase
from ..assets import get_image
from ..settings import width, height


class MenuBase(ScreenBase):

    _button_positions: list = [(width / 2, (height / 8) * (i + 3)) for i in range(4)]
    _row: int = height / 8
    _button_images: list = list()

    @property
    def row(self) -> int:
        """the value of screen height / 8"""
        return self._row

    def __init__(self, title: str, buttons: tuple[int]) -> None:
        super().__init__()
        MenuBase._button_images = get_image("buttons")

        self.title, self.title_rect = self.create_title(title)
        self.buttons: list[Button] = self.create_image_buttons(buttons)
        self.button_blit_seq = self._get_blitseq(self.buttons)

    def _get_blitseq(self, seq: list[any]) -> Sequence[Tuple[Surface, Rect]]:
        """
        list can contain any class with a
        image: pygame.Surface and a
        rect: pygame.Rect
        """
        return [(button.image, button.rect) for button in seq]

    def get_button_img(self, key: int) -> Surface:
        try:
            return self._button_images[key]
        except (KeyError, IndexError) as ex:
            raise ex.with_traceback()

    def create_title(self, title: str) -> tuple[Surface, Rect]:
        """Create menu title text"""
        _font = font.SysFont(None, 80, bold=True)
        title_image = _font.render(title, True, (255, 255, 255))
        title_rect = title_image.get_rect()
        title_rect.centerx = width / 2
        title_rect.centery = self._row * 2
        return (title_image, title_rect)

    def create_buttons(self, names: list[str]) -> list:
        """0 index will be the top button"""
        return [
            Button(name, pos=self._button_positions[i])
            for i, name in enumerate(names, 1)
        ]

    def create_image_buttons(self, img_keys: tuple[int]) -> list:
        return [
            ImageButton(_image, img_keys[i - 1], pos=self._button_positions[i])
            for i, _image in enumerate(
                [self.get_button_img(_key) for _key in img_keys], 1
            )
        ]


class Button:

    image: Surface = None
    rect: Rect = None
    name: str = None

    def __init__(
        self,
        button_text: str,
        size: tuple = (150, 50),
        font_size: int = 40,
        pos: tuple[int, int] = (0, 0),
    ):
        """
        surface: Surface -> Menu image,
        button_text: str -> text to display on top of button,
        size: tuple -> (width, height),
        font_size: int -> size of the text font,
        name: str -> uniqe string identifier
        """
        self.width, self.height = size

        self.image = Surface(size).convert_alpha()
        self.image.fill((144, 144, 144, 255))
        self.rect = self.image.get_rect()
        self.name = button_text

        self.set_text(button_text, font_size)
        self.set_position(pos)

    def set_text(
        self,
        text: str,
        font_size: int,
        text_color=(225, 225, 225, 255),
        bg_color=(144, 144, 144, 255),
    ):
        """set the buttons msg_text and msg_text_rect"""
        text_font = font.SysFont(None, font_size, bold=True)
        msg_image = text_font.render(text, True, text_color, bg_color)
        offset = (
            int((self.rect.width - msg_image.get_width()) / 2),
            int((self.rect.height - msg_image.get_height()) / 2),
        )
        self.image.fill(bg_color)
        self.image.blit(msg_image, offset)

    def check_button(self, mouse_pos, mouse_up: bool = False) -> bool:
        """check for button collision"""
        # If cursor is over the button when clicked
        if self.rect.collidepoint(mouse_pos):
            # if the mouse button was released over the button
            # and the button was the one pressed down on
            if mouse_up:
                if self.image.get_alpha() < 255:
                    self.reset_alpha()
                    return True
                # if the mouse button was release over this button
                # but a different button was clicked
                return False
            else:
                self.image.set_alpha(25)
        # if user releases the mouse button and this button
        # was the one that was pressed
        elif mouse_up:
            self.reset_alpha()

    def reset_alpha(self):
        self.image.set_alpha(255)

    def set_position(self, x_pos: Union[int, tuple] = None, y_pos: int = None):
        """Set the position of the rect"""
        if isinstance(x_pos, tuple):
            self.rect.center = x_pos
        else:
            if x_pos:
                self.rect.x = x_pos
            if y_pos:
                self.rect.y = y_pos


class ImageButton(Button):

    __image: Surface = None
    __key: int = None

    @property
    def image(self) -> Surface:
        return self.__image

    @image.setter
    def image(self, val: Surface):
        if isinstance(val, Surface):
            self.__image = val
        else:
            traceback.print_stack()
            raise TypeError(f"ERROR: Value -> {val} not a Surface!")

    @property
    def key(self) -> int:
        return self.__key

    @key.setter
    def key(self, val: int):
        if isinstance(val, int):
            self.__key = val
        else:
            traceback.print_stack()
            raise TypeError(f"TypeError: Value -> {val} not an integer!")

    def __init__(self, img: Surface, key: int, pos: tuple) -> None:
        self.image = img
        self.rect = self.image.get_rect()
        self.set_position(pos)
        self.key = key
