import os

from ..settings import size

from abc import ABCMeta
from pygame import Surface
from pygame import event


class ScreenBase(metaclass=ABCMeta):
    """
    Store all of the code every screen in the game will need access to
    """

    # bool to tell the main loop to reassign the active screen
    change_screen: bool = False
    # next active screen's key | First active screen is main menu
    # screen's key will be the file name of the screen without ".py"
    next_screen: str = "main_menu"

    sound_path: str = os.path.join(os.getcwd(), "assets/sound")

    width, height = size

    CHANGESCREEN: int = event.custom_type()
    PAUSE: int = event.custom_type()

    def __init__(self) -> None:
        self.image = Surface(size).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "check_events")
            and callable(subclass.check_events)
            and hasattr(subclass, "update")
            and callable(subclass.update)
            and hasattr(subclass, "change_screen")
            and callable(subclass.change_screen)
        )
