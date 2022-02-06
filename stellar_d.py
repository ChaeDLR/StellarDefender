import pygame
import src
from sys import exit


class StellarDefender:
    def __init__(self):
        pygame.init()
        self.main_screen = pygame.display.set_mode(
            src.size, flags=pygame.SCALED, vsync=1
        )

        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.TEXTINPUT])

        self.state = src.State()
        self.clock = pygame.time.Clock()

    def run_game(self):
        """runs the main loop of the game"""
        while 1:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                else:
                    self.state.check_events(event)

            self.state.update()
            self.state.draw(self.main_screen)

            pygame.display.update()


if __name__ == "__main__":
    stellar_defender = StellarDefender()
    stellar_defender.run_game()
