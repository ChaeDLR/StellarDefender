import pygame
import game
from sys import exit


class SpaceGame:
    width, height = game.screen_dims

    def __init__(self):
        pygame.init()
        self.main_screen = pygame.display.set_mode(
            (self.width, self.height), flags=pygame.DOUBLEBUF
        )
        self.screens = {
            "main_menu": game.MainMenu,
            "level": game.Level,
            "game_over": game.GameOver,
        }

        game.AssetManager.get_sprite_images()

        self.active_screen = self.screens["main_menu"]()
        self.clock = pygame.time.Clock()

    def __get_active_screen(self):
        """
        Get the new screen and return it
        """
        return self.screens[self.active_screen.new_screen]()

    def __check_events(self):
        """Check pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            else:
                self.active_screen.check_events(event)

    def run_game(self):
        """runs the main loop of the game"""
        while 1:
            self.clock.tick(60)
            if self.active_screen.change_screen:
                self.active_screen = self.__get_active_screen()
                self.change_screen = False

            self.__check_events()
            self.active_screen.update()
            self.main_screen.blit(self.active_screen.image, self.active_screen.rect)
            pygame.display.update()


if __name__ == "__main__":
    spaceGame = SpaceGame()
    spaceGame.run_game()
