# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import math
import arcade
import random

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Welcome to Arcade"
RADIUS = 10 
BLUE_IMG = "./assets/blue.png"
RED_IMG = "./assets/red.png"
PURPLE_IMG = "./assets/purple.png"

STEP_SIZE = 3

HALF_PI = math.pi / 2
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
        self.blue_entity = Entity(BLUE_IMG, direction_bias=(-1, -1), center_x= 50, center_y=30)
        self.red_entity = Entity(RED_IMG, center_x= 150, center_y=130)
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
        if arcade.check_for_collision(self.red_entity, self.blue_entity):
            print("Collision detected!")
        # self.blue_entity.move(1, 0)
        self.blue_entity.update()
        self.red_entity.update()
        self.food_entity.update([self.blue_entity])

# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()
