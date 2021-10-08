from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame import event
from .menu_base import MenuBase
from .components.button import Button


class GameOver(MenuBase):
    def __init__(self):

        self.title, self.title_rect = self.create_title("GAME OVER")

        self.main_menu_button = Button("Main Menu", font_size=35)
        midx: int = (self.rect.width / 2) - self.main_menu_button.rect.width / 2
        self.main_menu_button.set_position(
            x_pos=midx,
            y_pos=(self.rect.height / 2),
        )

        self.retry_button = Button("Retry")
        self.retry_button.set_position(
            x_pos=midx,
            y_pos=(self.rect.height / 2) + 100,
        )

        self.quit_button = Button("Quit")
        self.quit_button.set_position(
            x_pos=midx,
            y_pos=(self.rect.height / 2) + 200,
        )

    def __check_mousedown_events(self, mouse_pos):
        self.main_menu_button.check_button(mouse_pos)
        self.retry_button.check_button(mouse_pos)
        self.quit_button.check_button(mouse_pos)

    def __check_mouseup_events(self, mouse_pos):
        if self.main_menu_button.check_button(mouse_pos, True):
            self.change_screen = True
            self.new_screen = "main_menu"
        elif self.retry_button.check_button(mouse_pos, True):
            self.change_screen = True
            self.new_screen = "level_one"
        elif self.quit_button.check_button(mouse_pos, True):
            event.clear()
            event.post(event.Event(QUIT))

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.__check_mousedown_events(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_mouseup_events(event.pos)

    def update(self):
        self.image.fill((1, 1, 1))
        self.image.blit(self.title, self.title_rect)
        self.image.blit(self.main_menu_button.image, self.main_menu_button.rect)
        self.image.blit(self.retry_button.image, self.retry_button.rect)
        self.image.blit(self.quit_button.image, self.quit_button.rect)
