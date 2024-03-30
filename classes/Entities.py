import math
import arcade
from classes.Config import Config
from classes.Environment import Environment
from constants import PURPLE_IMG, SCREEN_HEIGHT, SCREEN_WIDTH


class Entity(arcade.Sprite):
    def __init__(
        self,
        environment: Environment,
        image,
        center_x=0,
        center_y=0,
        angle=0,
        **kwargs,
    ):
        super().__init__(
            image,
            scale=3,
            center_x=center_x,
            center_y=center_y,
            hit_box_algorithm=None,
            **kwargs,
        )
        self.environment = environment
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
        if self.center_x < 0:
            self.turn(180 - self.angle)
            self.center_x = 0
        if self.center_y < 0:
            self.turn(360 - self.angle)
            self.center_y = 0
        if self.center_x > SCREEN_WIDTH:
            self.turn(180 - self.angle)
            self.center_x = SCREEN_WIDTH

        if self.center_y > SCREEN_HEIGHT:
            self.turn(360 - self.angle)
            self.center_y = SCREEN_HEIGHT

    def update(self):
        """
        Update the entity's position and check
        for collisions with the screen
        """
        self.check_for_collision_with_screen()
        return super().update()


class Herbivore(Entity):
    def __init__(
        self,
        environment: Environment,
        image,
        center_x=0,
        center_y=0,
        angle=0,
        **kwargs,
    ):
        super().__init__(
            environment=environment,
            image=image,
            center_x=center_x,
            center_y=center_y,
            angle=angle,
            **kwargs,
        )
        self.vision_radius = 50
        self.energy = 1000

    def update(self):
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

        plants = arcade.check_for_collision_with_list(
            self, self.environment.plants
        )

        for plant in plants:
            if Config.can_eat:
                self.eat(plant)

        # Update the entity's position and sprite
        super().update()

    def eat(self, plant: "Plant"):
        """
        !TODO:
        """
        self.energy += plant.energy
        plant.kill()

    def kill(self):
        """
        Set is_alive to False and call the parent's kill method
        """
        self.is_alive = False
        return super().kill()


class Carnivore(Entity):
    def __init__(
        self,
        environment: Environment,
        image,
        center_x=0,
        center_y=0,
        angle=0,
        **kwargs,
    ):
        super().__init__(
            environment=environment,
            image=image,
            center_x=center_x,
            center_y=center_y,
            angle=angle,
            **kwargs,
        )
        self.vision_radius = 50
        self.energy = 1000

    def update(self):
        # Check for collisions with the screen and decrease energy
        self.check_for_collision_with_screen()
        self.energy -= 2
        # Kill entity if energy is too low
        if Config.is_mortal and self.energy <= 0:
            self.kill()

        herbs = arcade.check_for_collision_with_list(
            self, self.environment.herbivores
        )
        for herb in herbs:
            if Config.can_eat:
                self.eat(herb)
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
    def __init__(
        self, environment: Environment, center_x=0, center_y=0, **kwargs
    ):
        super().__init__(
            environment=environment,
            image=PURPLE_IMG,
            center_x=center_x,
            center_y=center_y,
            **kwargs,
        )
        self.energy = 100

    def kill(self):
        self.is_alive = False
        return super().kill()

    def update(self):
        pass
