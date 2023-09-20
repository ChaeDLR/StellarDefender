from pygame import font, Surface, Rect, SRCALPHA

from .surface_components import ProgressBar, TextSurface


class Hud:
    health_bar: ProgressBar = None
    score: TextSurface = None

    __score: int = 0
    __viewport_dims: tuple[int, int] = None

    def __init__(self, dims: tuple[int, int]) -> None:
        self.__viewport_dims = dims
        self.health_bar = ProgressBar((200, 30), (210, 20, 40, 255))
        self.score = TextSurface((240, 40), 56)

        self.health_bar.rect.center = dims[0] // 3, dims[1] - self.health_bar.rect.h
        self.score.rect.center = (dims[0] // 3) * 2, self.health_bar.rect.y

    def update_score(self, change: int) -> None:
        ...
