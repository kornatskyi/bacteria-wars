# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import math
import arcade
import random
from classes.Environment import Environment
from classes.Entities import Herbivore, Plant, Carnivore
from classes.QuadTree import QuadTree
from constants import *


class EntityManager:
    def __init__(self):
        self.environment = Environment()
        self.init_state = {
            "Carnivore": 30,
            "Herbivore": 30,
            "Plant": 10,
        }
        self.qt = QuadTree(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    def create_entities(self):
        for entity_type in self.init_state.keys():
            entities = [
                self.create_entity(entity_type)
                for _ in range(self.init_state[entity_type])
            ]
            self.environment.entities.extend(entities)

    def create_entity(self, entity_type: str):
        # Simplified entity creation logic
        # You can expand this to include your specific entity creation logic
        if entity_type == "Carnivore":
            return Carnivore(
                RED_IMG,
                center_x=random.random() * SCREEN_WIDTH,
                center_y=random.random() * SCREEN_HEIGHT,
                movement_angle=random.random() * 2 * math.pi,
            )
        if entity_type == "Herbivore":
            return Herbivore(
                BLUE_IMG,
                center_x=random.random() * SCREEN_WIDTH,
                center_y=random.random() * SCREEN_HEIGHT,
                movement_angle=random.random() * 2 * math.pi,
            )
        if entity_type == "Plant":
            return Plant(
                center_x=random.random() * SCREEN_WIDTH,
                center_y=random.random() * SCREEN_HEIGHT,
            )

    def update_entities(self):
        self.qt.clear()
        for entity in self.environment.entities:
            # populate quad tree
            self.qt.insert(entity)
        # Update and manage entities here
        for entity in self.environment.entities:
            if not entity.is_alive:
                self.environment.entities.remove(entity)
            else:
                # Update entity, inject any necessary environment information
                if isinstance(entity, Carnivore):
                    entity.update(self.qt)
                elif isinstance(entity, Herbivore):
                    entity.update(self.qt)
                else:
                    entity.update()


class World(arcade.Window):
    """Main welcome window"""

    def __init__(self):
        """Initialize the window"""

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.set_location(100, 1000)  # Change 100, 100 to your desired coordinates

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

        self.entity_manager = EntityManager()
        self.entity_manager.create_entities()

    def on_draw(self):
        """Called whenever you need to draw your window"""

        # Clear the screen and start drawing
        arcade.start_render()
        self.entity_manager.qt.root.draw(arcade)  # draw quads

        for entity in self.entity_manager.environment.entities:
            entity.draw()

        arcade.finish_render()

    def update(self, delta_time):
        self.entity_manager.update_entities()
        pass


# Main code entry point
if __name__ == "__main__":
    app = World()
    arcade.run()
