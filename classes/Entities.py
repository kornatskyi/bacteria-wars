import math
import random
import arcade

from constants import HALF_PI, PURPLE_IMG


class Entity(arcade.Sprite):
    def __init__(self, image, center_x=0, center_y=0, scale=0.1, direction_bias=(0, 0)):
        super().__init__(image, scale, center_x=center_x,center_y=center_y)
        # initial position
        self.direction_bias = direction_bias
        
    def move(self, change_x, change_y):
        if self.direction_bias:
            # calculate the angle between the current movement direction and the direction bias
            current_angle = math.atan2(change_y, change_x)
            bias_angle = math.atan2(self.direction_bias[1], self.direction_bias[0])
            angle_diff = bias_angle - current_angle

            # calculate the new movement vector with the direction bias
            new_angle = current_angle + angle_diff + HALF_PI - random.random() * math.pi
            speed = math.sqrt(change_x ** 2 + change_y ** 2)
            change_x = speed * math.cos(new_angle)
            change_y = speed * math.sin(new_angle)
        self.center_x += change_x
        self.center_y += change_y
        
    def check_for_collision_with_screen(self):
        viewport_left, viewport_right, viewport_bottom, viewport_top = arcade.get_viewport()
        if self.left < viewport_left:
            self.direction_bias = (1, self.direction_bias[1])
            self.left = viewport_left
        elif self.right > viewport_right:
            self.direction_bias = (-1, self.direction_bias[1])
            self.right = viewport_right
        if self.bottom < viewport_bottom:
            self.direction_bias = (self.direction_bias[0], 1)
            self.bottom = viewport_bottom
        elif self.top > viewport_top:
            self.direction_bias = (self.direction_bias[0], -1)
            self.top = viewport_top
            
    def draw(self):
        super().draw()

    def update(self):
        self.move(1, 1)
        self.check_for_collision_with_screen()
        return super().update()
    

class BlueEntity(Entity):
    def __init__(self, image, center_x=0, center_y=0, scale=0.1, direction_bias=(0, 0)):
        super().__init__(image, center_x, center_y, scale, direction_bias)
        self.vision_radius = 30
        
    def update(self, blue_entities: list[Entity]):
        closest_blue_entity = None
        closest_distance = 100
        for blue_entity in blue_entities:
            distance = math.sqrt((self.center_x - blue_entity.center_x) ** 2 + (self.center_y - blue_entity.center_y) ** 2)
            if distance < closest_distance:
                closest_distance = distance
                closest_blue_entity = blue_entity
        if closest_blue_entity:
            self.direction_bias = ((closest_blue_entity.center_x - self.center_x) / closest_distance, (closest_blue_entity.center_y - self.center_y) / closest_distance)
        self.check_for_collision_with_screen()
        super().update()
        pass

class RedEntity(Entity):
    def __init__(self, image, center_x=0, center_y=0, scale=0.1, direction_bias=(0, 0)):
        super().__init__(image, center_x, center_y, scale, direction_bias)
        self.vision_radius = 30
        
    def update(self, blue_entities: list[Entity]):
        closest_blue_entity = None
        closest_distance = 100
        for blue_entity in blue_entities:
            distance = math.sqrt((self.center_x - blue_entity.center_x) ** 2 + (self.center_y - blue_entity.center_y) ** 2)
            if distance < closest_distance:
                closest_distance = distance
                closest_blue_entity = blue_entity
        if closest_blue_entity:
            self.direction_bias = ((closest_blue_entity.center_x - self.center_x) / closest_distance, (closest_blue_entity.center_y - self.center_y) / closest_distance)
        self.check_for_collision_with_screen()
        super().update()
        pass

class Food(Entity):
    def __init__(self, center_x=0, center_y=0):
        super().__init__(PURPLE_IMG, center_x=center_x, center_y=center_y, scale=0.1)
        
    def update(self, blue_entities:list[Entity]):
        for blue_entity in blue_entities:
            if arcade.check_for_collision(blue_entity, self):
                # Blue entity has collided with food, give it a new direction bias
                blue_entity.direction_bias = (random.uniform(-1, 1), random.uniform(-1, 1))
                # Remove the food entity
                self.kill()
                break