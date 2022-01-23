import pygame

from typing import Sequence, Tuple, Union
from .screenbase import ScreenBase
from ..settings import width, height

from pygame.font import SysFont


class MenuBase(ScreenBase):

    __row: int = height / 8

    def __init__(self, title: str, buttons_: list[str]) -> None:
        super().__init__()
        self.title, self.title_rect = self.create_title(title)
        self.buttons: list[Button] = self.create_buttons(buttons_)
        self.button_blit_seq = self._get_blitseq(self.buttons)

    def _get_blitseq(
        self, seq: list[any]
    ) -> Sequence[Tuple[pygame.Surface, pygame.Rect]]:
        """list can contain any class with a image: pygame.Surface and a rect: pygame.Rect"""
        button_seq: list = []
        for item in seq:
            try:
                button_seq.append((item.image, item.rect))
                button_seq.append((item.msg_image, item.msg_image_rect))
            except:
                print("\nLOOP")
                print(f"Failed to add Button object to list")
                print(f"Not a valid button object -> {item}.")
        return button_seq

    @property
    def row(self) -> int:
        """the value of screen height /8"""
        return self.__row

    def create_title(self, title: str) -> tuple:
        """Create menu title text"""
        font = SysFont(None, 80, bold=True)
        title_image = font.render(title, True, (255, 255, 255))
        title_rect = title_image.get_rect()
        title_rect.centerx = width / 2
        title_rect.centery = self.__row * 2
        return (title_image, title_rect)

    def create_buttons(self, names: list[str]) -> list:
        """0 index will be the top button"""
        buttons: list[Button] = []
        for i, name in enumerate(names, 1):
            buttons.append(
                Button(
                    name,
                    pos=(
                        width / 2,  # x position but rect.centerx
                        self.__row * (i + 3),  # y position rect.centery
                    ),
                )
            )
        self.button_blit_seq = buttons
        return buttons

class Button:
    button_color: tuple = (144, 144, 144, 255)
    text_color: tuple = (255, 255, 255, 255)

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

        self.image = pygame.Surface(size, flags=pygame.SRCALPHA).convert_alpha()
        self.image.fill(self.button_color)
        self.rect = self.image.get_rect()
        self.name = button_text

        self.set_text(button_text, font_size)
        self.set_position(pos)

    def set_text(self, text: str, font_size: int):
        """set the buttons msg_text and msg_text_rect"""
        text_font = pygame.font.SysFont(None, font_size, bold=True)
        self.msg_image = text_font.render(
            text, True, self.text_color, self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

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
                self.image.set_alpha(25, pygame.RLEACCEL)
                self.msg_image.set_alpha(25, pygame.RLEACCEL)
        # if user releases the mouse button and this button
        # was the one that was pressed
        elif self.image.get_alpha() < 255 and mouse_up:
            self.reset_alpha()

    def reset_alpha(self):
        self.image.set_alpha(255, pygame.RLEACCEL)
        self.msg_image.set_alpha(255, pygame.RLEACCEL)

    def set_position(self, x_pos: Union[int, tuple], y_pos: int = None):
        """Set the position of the rect"""
        if isinstance(x_pos, tuple):
            self.rect.center = x_pos
        else:
            if x_pos:
                self.rect.x = x_pos
            if y_pos:
                self.rect.y = y_pos
        self.msg_image_rect.center = self.rect.center
