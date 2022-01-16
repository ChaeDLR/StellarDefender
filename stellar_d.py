import pygame
import src
from sys import exit


class StellarDefender:
    def __init__(self):
        pygame.init()
        self.main_screen = pygame.display.set_mode(
            src.screen_dims, flags=pygame.SCALED | pygame.SRCALPHA, vsync=1
        )
        src.Assets.init()

        self.screens = {
            "main_menu": src.MainMenu,
            "level": src.Level,
            "game_over": src.GameOver,
        }

        pygame.event.set_blocked([pygame.MOUSEMOTION])

        self.background = src.Background(src.screen_dims)
        self.active_screen = self.screens["main_menu"]()
        self.clock = pygame.time.Clock()

    def __get_active_screen(self):
        """
        Get the new screen and return it
        """
        return self.screens[self.active_screen.new_screen]()

    def run_game(self):
        """runs the main loop of the game"""
        while 1:
            self.clock.tick(60)
            if self.active_screen.change_screen:
                self.active_screen.change_screen = False
                self.active_screen = self.__get_active_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                else:
                    self.active_screen.check_events(event)

            self.background.update()
            self.active_screen.update()

            self.main_screen.blit(self.background.image, self.background.rect)
            self.main_screen.blit(self.active_screen.image, self.active_screen.rect)

            pygame.display.update()


if __name__ == "__main__":
    stellar_defender = StellarDefender()
    stellar_defender.run_game()
