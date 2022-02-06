import pygame

from .screens import *
from .assets import Assets
from .settings import size


class State:

    background: Background = Background(size)
    paused: bool = False

    def __init__(self):
        Assets.init()
        self.__active_screen = MainMenu()

        self.screens: dict = {
            "main_menu": MainMenu,
            "level": Level,
            "game_over": GameOver,
        }

    def check_events(self, event) -> None:
        if event.type == self.__active_screen.CHANGESCREEN:
            self.__active_screen = self.screens[self.__active_screen.next_screen]()
        else:
            self.__active_screen.check_events(event)

    def update(self) -> None:
        self.background.update()
        self.__active_screen.update()

    def draw(self, display: pygame.Surface) -> None:
        display.fill((0, 0, 0))
        display.blit(self.background.image, self.background.rect)
        display.blit(self.__active_screen.image, self.__active_screen.rect)
