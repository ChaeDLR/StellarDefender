from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame import event, mouse, cursors
from .components.button import Button
from .menu_base import MenuBase


class MainMenu(MenuBase):
    """
    Games main menu class
    """

    def __init__(self):

        self.title, self.title_rect = self.create_title("Stellar-D")

        # main menu buttons
        self.start_button = Button("Start")
        self.start_button.set_position(
            x_pos=(self.rect.width / 2) - self.start_button.rect.width / 2,
            y_pos=(self.rect.height / 2),
        )
        self.quit_button = Button("Quit")
        self.quit_button.set_position(
            x_pos=(self.rect.width / 2) - self.start_button.rect.width / 2,
            y_pos=(self.rect.height / 2) + 100,
        )

    def __check_mousedown_events(self, mouse_pos):
        """check for mousedown events"""
        self.start_button.check_button(mouse_pos)
        self.quit_button.check_button(mouse_pos)

    def __check_mouseup_events(self, mouse_pos):
        """check for mouseup events"""
        if self.start_button.check_button(mouse_pos, True):
            self.change_screen = True
            self.new_screen = "level"

        elif self.quit_button.check_button(mouse_pos, True):
            event.clear()
            event.post(event.Event(QUIT))

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.__check_mousedown_events(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_mouseup_events(event.pos)

    def update(self):
        self.background.update()
        self.image.blit(self.background.image, self.background.rect)
        self.image.blit(self.start_button.image, self.start_button.rect)
        self.image.blit(self.quit_button.image, self.quit_button.rect)
        self.image.blit(self.title, self.title_rect)
