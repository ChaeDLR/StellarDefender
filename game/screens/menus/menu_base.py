from ..screen_base import ScreenBase
from ...settings import width, height

from pygame.font import SysFont


class MenuBase(ScreenBase):
    def create_title(self, title: str) -> tuple:
        """Create menu title text"""
        font = SysFont(None, 80, bold=True)
        title_image = font.render(title, True, (255, 255, 255))
        title_rect = title_image.get_rect()
        title_rect.centerx = width / 2
        title_rect.centery = (height / 8) * 2
        return (title_image, title_rect)
