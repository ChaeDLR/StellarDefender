from ..screen_base import ScreenBase
from ...settings import width, height
from .components.button import Button

from pygame.font import SysFont


class MenuBase(ScreenBase):
    __row: int = height / 8

    def create_title(self, title: str) -> tuple:
        """Create menu title text"""
        font = SysFont(None, 80, bold=True)
        title_image = font.render(title, True, (255, 255, 255))
        title_rect = title_image.get_rect()
        title_rect.centerx = width / 2
        title_rect.centery = self.__row * 2
        return (title_image, title_rect)

    def create_buttons(self, names: list[str]) -> list[Button]:
        """names[0] will be the button"""
        buttons: list[Button] = []
        for i, name in enumerate(names, 1):
            buttons.append(Button(name, pos=(width / 2, (self.__row * i) + 100)))
        return buttons
