from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame import event, mouse

from ...base import MenuBase


class GameOver(MenuBase):
    def __init__(self):
        super().__init__("Game Over", ["Main Menu", "Retry", "Quit"])

        # adjust the main menu buttons font
        self.buttons[0].set_text("Main Menu", 32)
        self.button_blit_seq = self._get_blitseq(self.buttons)

        mouse.set_visible(True)

    def __check_mousedown_events(self, mouse_pos):
        """let the button know it's been pressed"""
        for button in self.buttons:
            button.check_button(mouse_pos)

    def __check_mouseup_events(self, mouse_pos):
        """execute the button's mapped command"""
        for button in self.buttons:
            if button.check_button(mouse_pos, True):
                if button.name == "Main Menu":
                    self.next_screen = "main_menu"
                    event.post(event.Event(self.CHANGESCREEN))
                elif button.name == "Retry":
                    self.next_screen = "level"
                    event.post(event.Event(self.CHANGESCREEN))
                elif button.name == "Quit":
                    event.clear()
                    event.post(event.Event(QUIT))

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.__check_mousedown_events(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_mouseup_events(event.pos)

    def update(self):
        self.image.fill((0, 0, 0))
        self.image.blit(self.title, self.title_rect)
        self.image.blits(self.button_blit_seq)
