from pygame import event
from pygame.constants import MOUSEBUTTONDOWN
from pygame.constants import MOUSEBUTTONUP

from .menu_base import MenuBase
from .components.button import Button

from sys import exit


class PauseMenu(MenuBase):
    def __init__(self):
        super().__init__("PAUSED", ["Resume", "Quit"])
        self.background_color = (
            10,
            10,
            10,
            55,
        )

    def __check_button_down(self, mouse_pos):
        for button in self.buttons:
            button.check_button(mouse_pos)

    def __check_button_up(self, mouse_pos):
        for button in self.buttons:
            if button.check_button(mouse_pos, True):
                if button.name == "Resume":
                    event.post(event.Event(self.PAUSE))
                elif button.name == "Quit":
                    exit()
        else:
            for button in self.buttons:
                button.reset_alpha()

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.__check_button_down(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_button_up(event.pos)

    def update(self):
        self.image.fill(self.background_color)
        self.image.blit(self.title, self.title_rect)
        self.image.blits(self.button_blit_seq)
