import math
import random
import arcade

from constants import HALF_PI, PURPLE_IMG


class Entity(arcade.Sprite):
    def __init__(self, image, center_x=0, center_y=0, scale=0.1):
        super().__init__(image, scale, center_x=center_x, center_y=center_y)
        # initial position
        self.speed = 5
        self.movement_angle = math.pi / 8

    def move(self):
        delta_x = self.speed * math.cos(self.movement_angle)
        delta_y = self.speed * math.sin(self.movement_angle)
        self.center_x += delta_x
        self.center_y += delta_y

    def check_for_collision_with_screen(self):
        viewport_left, viewport_right, viewport_bottom, viewport_top = arcade.get_viewport()
        if self.left < viewport_left:
            self.movement_angle = math.pi - self.movement_angle
            self.left = viewport_left
        elif self.right > viewport_right:
            self.movement_angle = math.pi - self.movement_angle
            self.right = viewport_right
        if self.bottom < viewport_bottom:
            self.movement_angle =  2 * math.pi - self.movement_angle
            self.bottom = viewport_bottom
        elif self.top > viewport_top:
            self.movement_angle = 2 * math.pi - self.movement_angle
            self.top = viewport_top

    def draw(self):
        super().draw()

    def update(self):
        self.move()
        self.check_for_collision_with_screen()
        return super().update()


class BlueEntity(Entity):
    def __init__(self, image, center_x=0, center_y=0, scale=0.1):
        super().__init__(image, center_x, center_y, scale)
        self.vision_radius = 30

    def update(self, red_entities: list["RedEntity"]):
        self.check_for_collision_with_screen()
        super().update()
        pass


class RedEntity(Entity):
    def __init__(self, image, center_x=0, center_y=0, scale=0.1):
        super().__init__(image, center_x, center_y, scale)
        self.vision_radius = 30

    def update(self, blue_entities: list[BlueEntity]):

        self.check_for_collision_with_screen()
        super().update()
        pass


class Food(Entity):
    def __init__(self, center_x=0, center_y=0):
        super().__init__(PURPLE_IMG, center_x=center_x, center_y=center_y, scale=0.1)

    def update(self, blue_entities: list[Entity]):
        for blue_entity in blue_entities:
            if arcade.check_for_collision(blue_entity, self):
                # Blue entity has collided with food, give it a new direction bias
                blue_entity.direction_bias = (
                    random.uniform(-1, 1), random.uniform(-1, 1))
                # Remove the food entity
                self.kill()
                break
