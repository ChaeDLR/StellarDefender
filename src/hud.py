from pygame import font, Surface, Rect, SRCALPHA

from surface_components import ProgressBar


class Hud:
    health_bar: ProgressBar = None
    score: Surface = None

    def __init__(self) -> None:
        self.health_bar = ProgressBar()
        self.score = Surface((240, 40), flags=SRCALPHA)

    def create_text(
        self,
        x_y: tuple,
        text: str,
        textsize: int = 56,
        boldtext: bool = True,
    ) -> tuple[Surface, Rect]:
        """
        x_y: tuple -> positions using center of the rect
        Tuple -> (text_img, text_rect)
        """
        text_font = font.SysFont(None, textsize, bold=boldtext)
        text_img = text_font.render(text, True, self.text_color)
        text_rect = text_img.get_rect()
        text_rect.center = x_y
        return (text_img, text_rect)
