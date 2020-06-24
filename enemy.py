import arcade
from arcade.sprite import *
import constants


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class Enemy(Sprite):
    def __init__(self, scale: float = 0.5,
                 image_x: float = 0, image_y: float = 0,
                 center_x: float = 0, center_y: float = 0):
        super().__init__(scale=scale, image_x=image_x, image_y=image_y,
                         center_x=center_x, center_y=center_y)
        self.enemy_direction = constants.LEFT_FACING
        self.cur_texture_index = 0
        self.texture_change_distance = 500

        self.stand_textures = load_texture_pair(f"{constants.ENEMY_MAIN_PATH}stand/0.png")
        self.walk_textures = []
        for i in range(10):
            texture = load_texture_pair(f"{constants.ENEMY_MAIN_PATH}walk/{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.stand_textures[0]
        self.set_hit_box(self.texture.hit_box_points)

        self.origin_x = self.center_x
        self.origin_y = self.center_y

    def update_animation(self, delta_time: float = 1/60):
        x1 = self.center_x
        x2 = self.origin_x
        y1 = self.center_y
        y2 = self.origin_y
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        if self.change_x == 0:
            self.texture = self.stand_textures[self.enemy_direction]
        elif distance > self.texture_change_distance:
            self.origin_x = self.center_x
            self.origin_y = self.center_y
            self.change_x = -self.change_x
            if self.enemy_direction == constants.RIGHT_FACING:
                self.enemy_direction = constants.LEFT_FACING
            elif self.enemy_direction == constants.LEFT_FACING:
                self.enemy_direction = constants.RIGHT_FACING

        self.cur_texture_index += 1
        if self.cur_texture_index > 9:
            self.cur_texture_index = 0
        self.texture = self.walk_textures[self.cur_texture_index][self.enemy_direction]
