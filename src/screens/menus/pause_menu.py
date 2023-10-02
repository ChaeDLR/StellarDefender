from pygame import event
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from ...base import MenuBase
from ...assets import keys


class PauseMenu(MenuBase):
    def __init__(self):
        super().__init__("PAUSED", [keys.buttons.play, keys.buttons.quit])
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
                if button.key == keys.buttons.play:
                    event.post(event.Event(self.PAUSE))
                elif button.key == keys.buttons.quit:
                    self.next_screen = "main_menu"
                    event.post(event.Event(self.CHANGESCREEN))
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
