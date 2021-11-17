from pygame import sprite, time
from game import settings

from ...sprites import Enemy
from ...asset_manager import AssetManager


class LevelOne:
    """
    Basic gameplay state with basic enemies
    """

    def __init__(self):
        self.group: sprite.Group = sprite.Group()
        self.enemy_img = AssetManager.sprite_images["enemy_ship"]
        img_width, img_height = self.enemy_img["image"].get_size()

        self.enemies: dict = {
            "lead": {
                "sprite": Enemy(self.enemy_img),
                "off-set-x": None,
                "off-set-y": int(img_height * 2.5),
            },
            "left_flank": {
                "sprite": Enemy(self.enemy_img),
                "off-set-x": int(img_width * 2.5),
                "off-set-y": int((img_height / 2) + 1),
            },
            "right_flank": {
                "sprite": Enemy(self.enemy_img),
                "off-set-x": int((img_width * 2.5) * -1),
                "off-set-y": int((img_height / 2) + 1),
            },
        }

        self.BASIC_ATK: int = 1000
        self.SPECIAL_ATK: int = 2500

        for position in self.enemies:
            self.__spawn_enemy(position)

    def __spawn_enemy(self, position: str):
        """
        Create a new enemy and add it to the sprite group at the given
        position in the formation
        """
        enemy: Enemy = self.enemies[position]["sprite"]
        enemy.set_position((settings.width / 2), -50)
        enemy.cancel_timers()
        time.set_timer(enemy.basic_atk_event, self.BASIC_ATK)
        time.set_timer(enemy.special_atk_event, self.SPECIAL_ATK)
        self.group.add(enemy)

    def update(self, player_x: int):
        """
        Update all of the sprites in self.enemies
        """
        for position in self.enemies:
            if self.group.has(sprite := self.enemies[position]["sprite"]):
                sprite.update(
                    player_x + self.enemies[position]["off-set-x"]
                    if self.enemies[position]["off-set-x"]
                    else player_x,
                    self.enemies[position]["off-set-y"]
                    if sprite.rect.centery < self.enemies[position]["off-set-y"]
                    else None,
                )
            else:
                self.__spawn_enemy(position)
