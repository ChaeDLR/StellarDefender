from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame import event, mouse
from .menu_base import MenuBase
from .components.button import Button


class GameOver(MenuBase):
    def __init__(self):
        super().__init__()

        self.title, self.title_rect = self.create_title("GAME OVER")

        # main menu font needs to be 35
        self.buttons: list[Button] = self.create_buttons(["Main Menu", "Retry", "Quit"])

        # adjust the main menu buttons font
        self.buttons[0].set_text("Main Menu", 35)

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
                    print("Switching to main menu")
                    self.change_screen = True
                    self.new_screen = "main_menu"
                elif button.name == "Retry":
                    print("switching to level")
                    self.change_screen = True
                    self.new_screen = "level"
                elif button.name == "Quit":
                    event.clear()
                    event.post(event.Event(QUIT))

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.__check_mousedown_events(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_mouseup_events(event.pos)

    def update(self):
        self.image.blit(self.title, self.title_rect)
        self.image.blits(self.button_blit_seq)
