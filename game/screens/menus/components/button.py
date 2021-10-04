from pygame import Surface, font, RLEACCEL, SRCALPHA


class Button:
    def __init__(
        self,
        button_text: str,
        size: tuple = (150, 50),
        font_size: int = 40,
        name: str = None,
    ):
        """
        surface: Surface -> Menu image,
        button_text: str -> text to display on top of button,
        size: tuple -> (width, height),
        font_size: int -> size of the text font,
        name: str -> uniqe string identifier
        """
        self.width, self.height = size
        self.image = Surface(size, SRCALPHA)
        self.rect = self.image.get_rect()
        self.text = button_text
        self.font_size = font_size
        self.button_color = (255, 255, 175, 255)
        self.text_color = (10, 20, 15, 255)
        self.name = name

        self.resize((self.width, self.height))

        self.image.fill(self.button_color)
        self.set_text(button_text, font_size)

    def resize(self, w_h: tuple):
        """
        Resize the buttone given the width, height tuple
        """
        pos = (self.rect.x, self.rect.y)
        self.image = Surface(w_h, SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill(self.button_color)
        self.rect.x, self.rect.y = pos

    def check_button(self, mouse_pos, mouse_up: bool = False) -> bool:
        """check for button collision"""
        if self.rect.collidepoint(mouse_pos):
            if mouse_up:
                self.reset_alpha()
                return True
            else:
                self.image.set_alpha(25, RLEACCEL)
                self.msg_image.set_alpha(25, RLEACCEL)
        elif mouse_up:
            self.reset_alpha()

    def reset_alpha(self):
        self.image.set_alpha(255, RLEACCEL)
        self.msg_image.set_alpha(255, RLEACCEL)

    def set_position(self, x_pos=None, y_pos=None):
        """Set the position of the button"""
        if x_pos:
            self.rect.x = x_pos
        if y_pos:
            self.rect.y = y_pos

        self.msg_image_rect.center = self.rect.center

    def clear_text(self):
        self.msg_image.fill(self.button_color)

    def set_text(self, txt: str, fontsize: int = None):
        self.text = txt
        if fontsize:
            self.font_size = fontsize
            self.text_font = font.SysFont(None, self.font_size, bold=True)
        self.msg_image = self.text_font.render(
            self.text, True, self.text_color, self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        self.image.blit(self.msg_image, self.msg_image_rect)

    def restore_text(self):
        """
        Display stored text value to the button surface
        """
        self.msg_image = self.text_font.render(
            self.text, True, self.text_color, self.button_color
        )

    def update(self):
        """respond to button presses"""
        pass
