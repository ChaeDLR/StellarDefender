from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, KEYDOWN
from pygame import event, time, mouse

from ...screens import Level
from ...base import MenuBase


class MainMenu(MenuBase):
    """
    Games main menu class
    """

    def __init__(self):
        super().__init__("Stellar-D", ["start", "quit"])
        self.next_screen: str = "level"
        mouse.set_visible(True)

    def __check_mousedown_events(self, mouse_pos):
        """check for mousedown events"""
        for button in self.buttons:
            button.check_button(mouse_pos)

    def __check_mouseup_events(self, mouse_pos):
        """check for mouseup events"""
        for button in self.buttons:
            if button.check_button(mouse_pos, True):
                if button.name == "start":
                    event.post(event.Event(self.CHANGESCREEN))
                elif button.name == "quit":
                    event.clear()
                    event.post(event.Event(QUIT))

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.__check_mousedown_events(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_mouseup_events(event.pos)

    def update(self):
        self.image.fill((0, 0, 0))
        self.image.blits(self.button_blit_seq)
        self.image.blit(self.title, self.title_rect)
