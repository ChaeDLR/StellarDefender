import pygame

from typing import Sequence, Tuple
from ..screen_base import ScreenBase
from ...settings import width, height
from .components.button import Button

from pygame.font import SysFont


class MenuBase(ScreenBase):

    __button_blit_seq: Sequence[Tuple[pygame.Surface, pygame.Rect]] = []

    __row: int = height / 8

    @property
    def button_blit_seq(self) -> Sequence[Tuple[pygame.Surface, pygame.Rect]]:
        return self.__button_blit_seq

    @button_blit_seq.setter
    def button_blit_seq(
        self, seq: list[any]
    ) -> Sequence[Tuple[pygame.Surface, pygame.Rect]]:
        """list can contain any class with a image: pygame.Surface and a rect: pygame.Rect"""
        for item in seq:
            try:
                self.__button_blit_seq.append((item.image, item.rect))
                self.__button_blit_seq.append((item.msg_image, item.msg_image_rect))
            except:
                print("\nLOOP")
                print(f"Failed to add Button object to list")
                print(f"Not a valid button object -> {item}.")

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

    def create_buttons(self, names: list[str]) -> list[Button]:
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
