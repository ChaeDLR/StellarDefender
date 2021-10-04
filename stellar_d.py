import pygame
from pygame.constants import DOUBLEBUF
import game


class SpaceGame:
    # class variables

    width, height = game.screen_dims

    def __init__(self):
        # this code runs when an instance of this object is called
        pygame.init()
        self.main_screen = pygame.display.set_mode(
            (self.width, self.height), flags=DOUBLEBUF
        )

        # bool values
        self.is_running = True

        # store all of the uncalled games screens in a dictionary
        # and define each screens key
        self.screens = {
            "main_menu": game.MainMenu,
            "level_one": game.LevelOne,
            # "game_over": game_files.GameOver
        }
        # assign the first screen of the game
        self.active_screen = self.screens["main_menu"]((self.width, self.height))
        self.clock = pygame.time.Clock()

    def __get_active_screen(self):
        """
        Use the active screens new_screen: str to get
        a new instance of the screen from the self.screens: dict
        """
        return self.screens[self.active_screen.new_screen]((self.width, self.height))

    def __check_events(self):
        """Check pygame events"""
        # get next event in the event queue
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.is_running = False
            else:
                self.active_screen.check_events(event)

    def run_game(self):
        """runs the main loop of the game"""
        while self.is_running:
            self.clock.tick(60)
            # change the screen if the screen managers bool is changed to true anywhere in the program
            if self.active_screen.change_screen:
                self.active_screen = self.__get_active_screen()
                self.change_screen = False

            self.__check_events()
            self.active_screen.update()
            self.main_screen.blit(self.active_screen.image, self.active_screen.rect)
            pygame.display.update()


# to change class variavle
if __name__ == "__main__":
    spaceGame = SpaceGame()
    spaceGame.run_game()
