from pygame import Surface, USEREVENT
from .laser import SLaser
from .ship import Ship


class Enemy(Ship):
    def __init__(self, surface: Surface) -> None:
        super().__init__(surface)

        self.health: int = 4
        self.alpha: int = 255
        # rate the alpha changes
        self.alpha_inc: int = -50

        # CUSTOM EVENTS
        self.basic_attack = USEREVENT + 1
        self.special_attack = USEREVENT + 2

    def __track_player(self, player_x: float):
        """
        enemy tracks player position
        play_x: float -> player.rect.centerx
        """
        if not player_x - 1 <= self.rect.centerx <= player_x + 1:
            # formula to move x towards player x
            inc_x = (player_x - self.rect.x) / 40

            self.x += inc_x
            self.rect.x = int(self.x)

    def create_laser(self):
        super().create_laser(1, self.rect.bottom)

    def create_special_laser(self):
        """
        Create a special attack laser object and add it to a sprite group
        """
        s_laser: SLaser = SLaser(1)
        s_laser.set_position(self.rect.midbottom[0], self.rect.midbottom[1])
        self.lasers.add(s_laser)

    def update(self, play_x: float):
        """
        Update enemy sprite
        """
        self.__track_player(play_x)
        self.lasers.update()
        super().update()
