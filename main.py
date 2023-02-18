# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import math
import arcade
import random
from classes.Entities import BlueEntity, Entity, Food, RedEntity
from constants import *


class Welcome(arcade.Window):
    """Main welcome window
    """

    def __init__(self):
        """Initialize the window
        """

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

        self.food_entities = [Food(
            center_x=random.random() * SCREEN_WIDTH,
            center_y=random.random() * SCREEN_HEIGHT,) for _ in range(10)]
        self.blue_entities = [BlueEntity(BLUE_IMG,
                                         center_x=random.random() * SCREEN_WIDTH,
                                         center_y=random.random() * SCREEN_HEIGHT,
                                         movement_angle=random.random() * 2 * math.pi) for _ in range(10)]
        # self.red_entity = RedEntity(RED_IMG, center_x= 130, center_y=250)
        # self.red_entity = Entity(RED_IMG)

    def action_on_all(entities, action):
        for entity in entities:
            action(self=entity)

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        arcade.start_render()

        for entity in self.blue_entities:
            entity.draw()
        for entity in self.food_entities:
            entity.draw()

        arcade.finish_render()

    def update(self, delta_time):
        # if arcade.check_for_collision(self.red_entity, self.blue_entity):
        # print("Collision detected!")
        # self.blue_entity.move(1, 0)
        # blue_entities = [self.blue_entity]
        # red_entities = [self.red_entity]
        # self.blue_entity.update()
        for entity in self.blue_entities:
            entity.update()
        for entity in self.food_entities:
            entity.update(self.blue_entities)
        # for blue_entity in self.blue_entities:
        #     blue_entity.update()
        # self.red_entity.update(blue_entities)


# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()
