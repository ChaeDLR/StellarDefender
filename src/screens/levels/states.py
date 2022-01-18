from pygame import event, sprite
from src import settings

from ...sprites import Enemy, Saucer


class LevelOne:
    """
    Basic gameplay state with basic enemies
    """

    def __init__(self):
        self.group: sprite.Group = sprite.Group()

        img_width, img_height = Enemy.size

        self.enemies: dict = {
            "lead": {
                "sprite": Enemy(),
                "off-set-x": None,
                "off-set-y": int(img_height * 3.5),
            },
            "left_flank": {
                "sprite": Enemy(
                    1250,
                ),
                "off-set-x": int(img_width * 2.5),
                "off-set-y": int(img_height * 2.5),
            },
            "right_flank": {
                "sprite": Enemy(
                    1500,
                ),
                "off-set-x": int((img_width * 2.5) * -1),
                "off-set-y": int(img_height * 2.5),
            },
            "rear": {
                "sprite": Saucer(),
                "off-set-x": 0,
                "off-set-y": int((img_height / 2) + 1),
            },
        }

        for position in self.enemies:
            self.__spawn_enemy(position)

    def __spawn_enemy(self, position: str):
        """
        Create a new enemy and add it to the sprite group at the given
        position in the formation
        """
        enemy: Enemy = self.enemies[position]["sprite"]
        enemy.image.set_alpha(255)
        enemy.health = 4
        enemy.dying = False
        enemy.set_position((settings.width / 2), -50)
        enemy.attack()
        self.group.add(enemy)

    def pause(self) -> None:
        """pause the states active timers"""
        for enemy in self.group:
            enemy.capture_attack_timers()

    def unpause(self) -> None:
        for enemy in self.group:
            enemy.resume()

    def check_events(self, event: event.Event):
        """Check state specific events"""
        # attack events
        if hasattr(event, "attack"):
            event.attack()

    def update(self, player_x: int):
        """
        Update all of the sprites in self.enemies
        """
        for position in self.enemies:
            if self.group.has(enemy := self.enemies[position]["sprite"]):
                if enemy.health > 0:
                    self.enemies[position]["sprite"].update(
                        player_x + self.enemies[position]["off-set-x"]
                        if self.enemies[position]["off-set-x"]
                        else player_x,
                        self.enemies[position]["off-set-y"]
                        if self.enemies[position]["sprite"].rect.centery
                        < self.enemies[position]["off-set-y"]
                        else None,
                    )
                elif enemy.dying:
                    enemy.update_particles()
            else:
                self.__spawn_enemy(position)
