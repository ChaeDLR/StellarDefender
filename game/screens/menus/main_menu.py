import pygame
import sys

from ..background import Background
from .components.button import Button
from ..screen_base import ScreenBase


class MainMenu(ScreenBase):
    """
    Games main menu class
    """

    def __init__(self, w_h: tuple):
        self.image = pygame.Surface(w_h)
        self.rect = self.image.get_rect()
        self.background = Background(w_h)

        # main menu buttons
        self.start_button = Button("Start", name="start")
        self.start_button.set_position(
            x_pos=(self.rect.width / 2) - self.start_button.rect.width / 2,
            y_pos=(self.rect.height / 2),
        )
        self.quit_button = Button("Quit", name="quit")
        self.quit_button.set_position(
            x_pos=(self.rect.width / 2) - self.start_button.rect.width / 2,
            y_pos=(self.rect.height / 2) + 100,
        )

        self.title, self.title_rect = self.__create_title()

        # Ensure the mouse is set to the menu mouse
        pygame.mouse.set_cursor(pygame.cursors.arrow)

    def __create_title(self) -> tuple:
        """Create main menu title text"""
        title: str = "Stellar D"
        font = pygame.font.SysFont(None, 80, bold=True)
        title_image = font.render(title, True, (255, 255, 255))
        title_rect = title_image.get_rect()
        title_rect.centerx = self.rect.centerx
        title_rect.y += 250
        return (title_image, title_rect)

    def __check_mousedown_events(self, event):
        """check for mousedown events"""
        self.start_button.check_button(event.pos)
        self.quit_button.check_button(event.pos)

    def __check_mouseup_events(self, event):
        """check for mouseup events"""

        if self.start_button.check_button(event.pos, True):
            self.change_screen = True
            self.new_screen = "level_one"

        elif self.quit_button.check_button(event.pos, True):
            sys.exit()

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.__check_mousedown_events(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.__check_mouseup_events(event)

    def update(self):
        self.background.update()
        self.image.blit(self.background.image, self.background.rect)
        self.image.blit(self.start_button.image, self.start_button.rect)
        self.image.blit(self.quit_button.image, self.quit_button.rect)
        self.image.blit(self.title, self.title_rect)
