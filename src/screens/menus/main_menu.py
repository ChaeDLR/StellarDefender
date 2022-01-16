from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame import event
from .components.button import Button
from .menu_base import MenuBase


class MainMenu(MenuBase):
    """
    Games main menu class
    """

    def __init__(self):
        super().__init__()

        self.title, self.title_rect = self.create_title("Stellar-D")

        self.buttons: list[Button] = self.create_buttons(["start", "quit"])

    def __check_mousedown_events(self, mouse_pos):
        """check for mousedown events"""
        for button in self.buttons:
            button.check_button(mouse_pos)

    def __check_mouseup_events(self, mouse_pos):
        """check for mouseup events"""
        for button in self.buttons:
            if button.check_button(mouse_pos, True):
                if button.name == "start":
                    self.change_screen = True
                    self.new_screen = "level"
                elif button.name == "quit":
                    event.clear()
                    event.post(event.Event(QUIT))

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.__check_mousedown_events(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_mouseup_events(event.pos)

    def update(self):
        self.image.blits(self.button_blit_seq)
        self.image.blit(self.title, self.title_rect)
