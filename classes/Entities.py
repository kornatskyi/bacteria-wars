import math
import arcade
from classes.Config import Config
from classes.QuadTree import QuadTree
from classes.Utils import (
    Point,
    angle_between_x_axis_and_line_through_points,
    distance_between_two_points,
)
from constants import PURPLE_IMG


class Entity(arcade.Sprite):
    def __init__(self, image, center_x=0, center_y=0, angle=0, **kwargs):
        super().__init__(
            image,
            scale=5,
            center_x=center_x,
            center_y=center_y,
            hit_box_algorithm=None,
            **kwargs,
        )
        # initial position
        self.angle = angle
        self.speed = 5
        self.energy = 100
        self.is_alive = True
        # Set init speed and angle
        self.forward(self.speed)
        self.turn(self.angle)

    def turn(self, angle: float):
        """
        updates speed and rotates the sprite
        parameters: angle - in degrees
        """
        self.angle = angle
        self.change_x = self.speed * math.cos(self.radians)
        self.change_y = self.speed * math.sin(self.radians)

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
            self.turn(180 - self.angle)
            self.left = viewport_left
        elif self.right > viewport_right:
            self.turn(180 - self.angle)
            self.right = viewport_right
        if self.bottom < viewport_bottom:
            self.turn(360 - self.angle)
            self.bottom = viewport_bottom
        elif self.top > viewport_top:
            self.turn(360 - self.angle)
            self.top = viewport_top

    def draw(self):
        super().draw()
        self.draw_hit_box()

    def update(self):
        """
        Update the entity's position and check
        for collisions with the screen
        """
        self.check_for_collision_with_screen()
        return super().update()


class Herbivore(Entity):
    def __init__(self, image, center_x=0, center_y=0, angle=0, **kwargs):
        super().__init__(
            image=image,
            center_x=center_x,
            center_y=center_y,
            angle=angle,
            **kwargs,
        )
        self.vision_radius = 50
        self.energy = 1000

    def update(self, qt: QuadTree):
        """
        Update the blue entity's position, energy,
        and actions based on its surroundings.
        """
        # Check for collisions with the screen and decrease energy
        self.check_for_collision_with_screen()
        self.energy -= 2
        # Kill entity if energy is too low
        if Config.is_mortal and self.energy <= 0:
            self.kill()

        nearby_entities = qt.retrieve(self)
        for entity in nearby_entities:
            # Eat plant entities
            if isinstance(entity, Plant):
                ate = self.eat(entity)
                if not ate:
                    self_center = Point(self.center_x, self.center_y)
                    plant_entity_center = Point(
                        entity.center_x, entity.center_y
                    )
                    if (
                        # Chase after food entities
                        distance_between_two_points(
                            self_center, plant_entity_center
                        )
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
        Check for collisions with a plant entity
        and increase energy accordingly
        If ate return True else False
        """
        if arcade.check_for_collision(plant, self) and Config.can_eat:
            self.energy += plant.energy
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
    def __init__(self, image, center_x=0, center_y=0, angle=0, **kwargs):
        super().__init__(
            image=image,
            center_x=center_x,
            center_y=center_y,
            angle=angle,
            **kwargs,
        )
        self.vision_radius = 50
        self.energy = 1000

    def update(self, qt: QuadTree):
        # Check for collisions with the screen and decrease energy
        self.check_for_collision_with_screen()
        self.energy -= 2
        # Kill entity if energy is too low
        if Config.is_mortal and self.energy <= 0:
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
        Check for collisions with a plant entity
        and increase energy accordingly
        If ate return True else False
        """
        if arcade.check_for_collision(herbivore, self) and Config.can_eat:
            self.energy += herbivore.energy
            herbivore.kill()
            return True
        else:
            return False

    def kill(self):
        self.is_alive = False
        return super().kill()


class Plant(Entity):
    def __init__(self, center_x=0, center_y=0, **kwargs):
        super().__init__(
            PURPLE_IMG, center_x=center_x, center_y=center_y, **kwargs
        )
        self.energy = 100

    def kill(self):
        self.is_alive = False
        return super().kill()

    def update(self):
        pass
