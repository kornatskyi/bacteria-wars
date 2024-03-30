# Imports
import math
import arcade
import random
from classes.Config import Config
from classes.Environment import Environment
from classes.Entities import Herbivore, Plant, Carnivore
from constants import (
    BLUE_IMG,
    RED_IMG,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
)

# Dev imports
import cProfile


class EntityManager:
    def __init__(self):
        self.environment = Environment()

    def create_entities(self):
        for _ in range(Config.num_of_carnivores):
            self.environment.carnivores.append(self.create_entity("Carnivore"))
        for _ in range(Config.num_of_herbivores):
            self.environment.herbivores.append(self.create_entity("Herbivore"))
        for _ in range(Config.num_of_plants):
            self.environment.plants.append(self.create_entity("Plant"))

    def create_entity(self, entity_type: str):
        if entity_type == "Carnivore":
            return Carnivore(
                environment=self.environment,
                image=RED_IMG,
                center_x=random.random() * SCREEN_WIDTH,
                center_y=random.random() * SCREEN_HEIGHT,
                angle=math.degrees(random.random() * 2 * math.pi),
            )
        if entity_type == "Herbivore":
            return Herbivore(
                environment=self.environment,
                image=BLUE_IMG,
                center_x=random.random() * SCREEN_WIDTH,
                center_y=random.random() * SCREEN_HEIGHT,
                angle=math.degrees(random.random() * 2 * math.pi),
            )
        if entity_type == "Plant":
            return Plant(
                environment=self.environment,
                center_x=random.random() * SCREEN_WIDTH,
                center_y=random.random() * SCREEN_HEIGHT,
            )

    def update_entities(self):
        self.environment.carnivores.update()
        self.environment.herbivores.update()
        self.environment.plants.update()


class World(arcade.Window):
    """Main welcome window"""

    def __init__(self):
        """Initialize the window"""

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.set_location(
            100, 1000
        )  # Change 100, 100 to your desired coordinates

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

        self.entity_manager = EntityManager()
        self.entity_manager.create_entities()
        pass

    def on_draw(self):
        """Called whenever you need to draw your window"""

        # Clear the screen and start drawing
        arcade.start_render()
        self.entity_manager.environment.carnivores.draw()
        # self.entity_manager.environment.carnivores.draw_hit_boxes()
        self.entity_manager.environment.herbivores.draw()
        # self.entity_manager.environment.herbivores.draw_hit_boxes()
        self.entity_manager.environment.plants.draw()
        # self.entity_manager.environment.plants.draw_hit_boxes()

        arcade.finish_render()

    def update(self, delta_time):
        self.entity_manager.update_entities()
        pass


# Main code entry point
if __name__ == "__main__":
    app = World()

    cProfile.run("arcade.run()", "profile_data.prof")
