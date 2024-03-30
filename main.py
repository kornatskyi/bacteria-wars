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
import collections
import time
import timeit


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


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

        # Performance measurers
        self.processing_time = 0
        self.draw_time = 0
        self.program_start_time = timeit.default_timer()
        self.fps = FPSCounter()

        pass

    def on_draw(self):
        """Called whenever you need to draw your window"""
        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        self.clear()
        self.entity_manager.environment.carnivores.draw()
        # self.entity_manager.environment.carnivores.draw_hit_boxes()
        self.entity_manager.environment.herbivores.draw()
        # self.entity_manager.environment.herbivores.draw_hit_boxes()
        self.entity_manager.environment.plants.draw()
        # self.entity_manager.environment.plants.draw_hit_boxes()

        # Display info on sprites
        output = f"Carnivores count: {len(self.entity_manager.environment.carnivores):,}"
        arcade.draw_text(
            output,
            20,
            SCREEN_HEIGHT - 20,
            arcade.color.BLACK,
            16,
            bold=True,
        )

        # Display timings
        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(
            output,
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.BLACK,
            16,
            bold=True,
        )

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(
            output,
            20,
            SCREEN_HEIGHT - 60,
            arcade.color.BLACK,
            16,
            bold=True,
        )

        fps = self.fps.get_fps()
        output = f"FPS: {fps:3.0f}"
        arcade.draw_text(
            output,
            20,
            SCREEN_HEIGHT - 80,
            arcade.color.BLACK,
            16,
            bold=True,
        )

        self.draw_time = timeit.default_timer() - draw_start_time
        self.fps.tick()

    def update(self, delta_time):
        # Start update timer
        start_time = timeit.default_timer()

        self.entity_manager.update_entities()

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time
        pass


# Main code entry point
if __name__ == "__main__":
    app = World()

    cProfile.run("arcade.run()", "profile_data.prof")
