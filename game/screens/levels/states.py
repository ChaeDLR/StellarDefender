from pygame import Surface, event, sprite, time, image
from game import settings
from copy import deepcopy

from ...sprites import Enemy
from ...asset_manager import AssetManager


class LevelOne:
    """
    Basic gameplay state with basic enemies
    """

    def __init__(self):
        self.group: sprite.Group = sprite.Group()
        self.enemy_img: Surface = AssetManager.sprite_images["enemy_ship"]
        img_width, img_height = self.enemy_img["image"].get_size()
        enemy_imgstr: str = image.tostring(self.enemy_img["image"], "RGBA")

        self.enemies: dict = {
            "lead": {
                "sprite": Enemy(
                    {
                        "image": image.fromstring(
                            enemy_imgstr, (img_width, img_height), "RGBA"
                        ),
                        "colors": self.enemy_img["colors"],
                    }
                ),
                "off-set-x": None,
                "off-set-y": int(img_height * 2.5),
            },
            "left_flank": {
                "sprite": Enemy(
                    {
                        "image": image.fromstring(
                            enemy_imgstr, (img_width, img_height), "RGBA"
                        ),
                        "colors": self.enemy_img["colors"],
                    },
                    attack_speed=750,
                ),
                "off-set-x": int(img_width * 2.5),
                "off-set-y": int((img_height / 2) + 1),
            },
            "right_flank": {
                "sprite": Enemy(
                    {
                        "image": image.fromstring(
                            enemy_imgstr, (img_width, img_height), "RGBA"
                        ),
                        "colors": self.enemy_img["colors"],
                    },
                    attack_speed=750,
                ),
                "off-set-x": int((img_width * 2.5) * -1),
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
        enemy.cancel_timers()
        time.set_timer(enemy.basicatk_event, enemy.basicatk_event.speed)
        time.set_timer(enemy.specialatk_event, enemy.specialatk_event.speed)
        self.group.add(enemy)

    def check_events(self, event: event.Event):
        """Check state specific events"""
        for enemy in self.group.sprites():
            if event.type == enemy.basicatk_event.type:
                event.sprite.create_laser()
            elif event.type == enemy.specialatk_event.type:
                event.sprite.create_special_laser()

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
