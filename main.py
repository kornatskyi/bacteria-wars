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
            
        self.food_entity = Food(center_x=200, center_y=200)
        self.blue_entity = BlueEntity(BLUE_IMG, center_x= 250, center_y=150)
        self.red_entity = RedEntity(RED_IMG, center_x= 150, center_y=250)
        # self.red_entity = Entity(RED_IMG)

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        arcade.start_render()

        self.blue_entity.draw()
        self.red_entity.draw()
        self.food_entity.draw()

        arcade.finish_render()
        
    def update(self, delta_time):
        print(delta_time)
        if arcade.check_for_collision(self.red_entity, self.blue_entity):
            print("Collision detected!")
        # self.blue_entity.move(1, 0)
        blue_entities = [self.blue_entity]
        red_entities = [self.red_entity]
        self.blue_entity.update(red_entities)
        self.red_entity.update(blue_entities)
        self.food_entity.update(blue_entities)

# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()
