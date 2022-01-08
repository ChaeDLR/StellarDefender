from pygame import SRCALPHA
from pygame import mouse
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from .menu_base import MenuBase
from .components.button import Button

from typing import Callable


class PauseMenu(MenuBase):
    def __init__(self, unpause_func: Callable):
        super().__init__()
        self.background_color = (
            10,
            10,
            10,
            175,
        )
        self.unpause_function = unpause_func

        self.text_image, self.text_image_rect = self.create_title("PAUSED")

        self.buttons: list[Button] = self.create_buttons(["Resume", "Quit"])

    def __check_button_down(self, mouse_pos):
        for button in self.buttons:
            button.check_button(mouse_pos)

    def __check_button_up(self, mouse_pos):
        for button in self.buttons:
            if button.check_button(mouse_pos, True):
                if button.name == "resume":
                    self.unpause_function()
                elif button.name == "quit":
                    self.change_screen = True
                    self.new_sceen = "main_menu"
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
        self.image.blit(self.text_image, self.text_image_rect)

        for button in self.buttons:
            self.image.blit(button.image, button.rect)
