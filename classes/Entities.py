import math
import random
import arcade
from classes.QuadTree import QuadTree
from classes.Utils import (
    Point,
    angle_between_x_axis_and_line_through_points,
    distance_between_two_points,
)

from constants import HALF_PI, PURPLE_IMG


class Entity(arcade.Sprite):
    def __init__(
        self,
        image,
        scale=0.1,
        center_x=0,
        center_y=0,
        movement_angle=math.pi / 2,
    ):
        super().__init__(image, scale, center_x=center_x, center_y=center_y)
        # initial position
        self.speed = 1
        self.movement_angle = movement_angle
        self.energy = 100
        self.is_alive = True

    def move(self):
        """
        Move the entity in the direction specified by the movement angle
        """
        delta_x = self.speed * math.cos(self.movement_angle)
        delta_y = self.speed * math.sin(self.movement_angle)
        self.center_x += delta_x
        self.center_y += delta_y

    def check_for_collision_with_screen(self):
        """
        Check if the entity has collided with the edge of the screen
        and adjust the movement angle accordingly
        """
        (
            viewport_left,
            viewport_right,
            viewport_bottom,
            viewport_top,
        ) = arcade.get_viewport()
        if self.left < viewport_left:
            self.movement_angle = math.pi - self.movement_angle
            self.left = viewport_left
        elif self.right > viewport_right:
            self.movement_angle = math.pi - self.movement_angle
            self.right = viewport_right
        if self.bottom < viewport_bottom:
            self.movement_angle = 2 * math.pi - self.movement_angle
            self.bottom = viewport_bottom
        elif self.top > viewport_top:
            self.movement_angle = 2 * math.pi - self.movement_angle
            self.top = viewport_top

    def draw(self):
        super().draw()

    def update(self):
        """
        Update the entity's position and check for collisions with the screen
        """
        self.move()
        self.check_for_collision_with_screen()
        return super().update()


class Herbivore(Entity):
    def __init__(
        self, image, center_x=0, center_y=0, scale=0.1, movement_angle=math.pi
    ):
        super().__init__(
            image=image,
            center_x=center_x,
            center_y=center_y,
            scale=scale,
            movement_angle=movement_angle,
        )
        self.vision_radius = 50
        self.energy = 1000

    def update(self, qt: QuadTree):
        """
        Update the blue entity's position, energy, and actions based on its surroundings.
        """
        # Check for collisions with the screen and decrease energy
        self.check_for_collision_with_screen()
        self.energy -= 2
        # Kill entity if energy is too low
        if self.energy <= 0:
            self.kill()

        nearby_entities = qt.retrieve(self)
        for entity in nearby_entities:
            # Eat plant entities
            if isinstance(entity, Plant):
                ate = self.eat(entity)
                if not ate:
                    self_center = Point(self.center_x, self.center_y)
                    plant_entity_center = Point(entity.center_x, entity.center_y)
                    if (
                        # Chase after food entities
                        distance_between_two_points(self_center, plant_entity_center)
                        < self.vision_radius
                    ):
                        self.movement_angle = (
                            angle_between_x_axis_and_line_through_points(
                                self_center, plant_entity_center
                            )
                        )

        # Update the entity's position and sprite
        super().update()

    def eat(self, plant: "Plant"):
        """
        Check for collisions with a plant entity and increase energy accordingly
        If ate return True else False
        """
        if arcade.check_for_collision(plant, self):
            self.energy += plant.energy
            # Remove the plant entity
            plant.kill()
            return True
        else:
            return False

    def kill(self):
        """
        Set is_alive to False and call the parent's kill method
        """
        self.is_alive = False
        return super().kill()


class Carnivore(Entity):
    def __init__(
        self, image, center_x=0, center_y=0, scale=0.1, movement_angle=math.pi
    ):
        super().__init__(
            image=image,
            center_x=center_x,
            center_y=center_y,
            scale=scale,
            movement_angle=movement_angle,
        )
        self.vision_radius = 50
        self.energy = 1000

    def update(self, qt: QuadTree):
        # Check for collisions with the screen and decrease energy
        self.check_for_collision_with_screen()
        self.energy -= 2
        # Kill entity if energy is too low
        if self.energy <= 0:
            self.kill()
        nearby_entities = qt.retrieve(self)
        # chase food
        for entity in nearby_entities:
            # Eat plant entities
            if isinstance(entity, Herbivore):
                ate = self.eat(entity)
                if not ate:
                    self_center = Point(self.center_x, self.center_y)
                    entity_center = Point(entity.center_x, entity.center_y)
                    if (
                        # Chase after food entities
                        distance_between_two_points(self_center, entity_center)
                        < self.vision_radius
                    ):
                        self.movement_angle = (
                            angle_between_x_axis_and_line_through_points(
                                self_center, entity_center
                            )
                        )
        super().update()

    def eat(self, herbivore: "Herbivore"):
        """
        Check for collisions with a plant entity and increase energy accordingly
        If ate return True else False
        """
        if arcade.check_for_collision(herbivore, self):
            self.energy += herbivore.energy
            # Remove the plant entity
            herbivore.kill()
            return True
        else:
            return False

    def kill(self):
        self.is_alive = False
        return super().kill()


class Plant(Entity):
    def __init__(self, center_x=0, center_y=0):
        super().__init__(PURPLE_IMG, center_x=center_x, center_y=center_y, scale=0.1)
        self.energy = 100

    def kill(self):
        self.is_alive = False
        return super().kill()

    def update(self):
        pass
