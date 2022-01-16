import pygame
from .menu_base import MenuBase
from .components.button import Button

from sys import exit
from typing import Callable


class PauseMenu(MenuBase):
    def __init__(self, unpause: Callable):
        super().__init__()
        self.background_color = (
            10,
            10,
            10,
            175,
        )
        self.unpause = unpause

        self.text_image, self.text_image_rect = self.create_title("PAUSED")

        self.buttons: list[Button] = self.create_buttons(["Resume", "Quit"])

    def __check_button_down(self, mouse_pos):
        for button in self.buttons:
            button.check_button(mouse_pos)

    def __check_button_up(self, mouse_pos):
        for button in self.buttons:
            if button.check_button(mouse_pos, True):
                if button.name == "Resume":
                    self.unpause()
                elif button.name == "Quit":
                    exit()
        else:
            for button in self.buttons:
                button.reset_alpha()

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.__check_button_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.__check_button_up(event.pos)

    def update(self):
        self.image.fill(self.background_color)
        self.image.blit(self.text_image, self.text_image_rect)
        self.image.blits(self.button_blit_seq)
