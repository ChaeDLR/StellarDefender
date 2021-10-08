from ..screen_base import ScreenBase

from pygame.font import SysFont


class MenuBase(ScreenBase):
    def create_title(self, title: str) -> tuple:
        """Create menu title text"""
        font = SysFont(None, 80, bold=True)
        title_image = font.render(title, True, (255, 255, 255))
        title_rect = title_image.get_rect()
        title_rect.centerx = self.rect.centerx
        title_rect.y += 250
        return (title_image, title_rect)
