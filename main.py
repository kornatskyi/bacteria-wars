# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Welcome to Arcade"
RADIUS = 10 
BLUE_IMG = "./assets/blue.png"
RED_IMG = "./assets/red.png"

class Entity(arcade.Sprite):
    def __init__(self, image, center_x=0, center_y=0, scale=0.1, border_color=arcade.color.BLACK, border_width=1):
        super().__init__(image, scale, center_x=center_x,center_y=center_y)
        self.border_color = border_color
        self.border_width = border_width
        # initial position
        
    def move(self, change_x, change_y):
        self.center_x += change_x
        self.center_y += change_y
        
    def check_for_collision_with_screen(self):
        viewport_left, viewport_right, viewport_bottom, viewport_top = arcade.get_viewport()
        if self.left < viewport_left:
            self.left = viewport_left
        elif self.right > viewport_right:
            self.right = viewport_right
        if self.bottom < viewport_bottom:
            self.bottom = viewport_bottom
        elif self.top > viewport_top:
            self.top = viewport_top
    
    def draw(self):
        super().draw()
        # border
        arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height, self.border_color, self.border_width)

    def update(self):
        self.move(random.random() - 0.5, random.random()- 0.5)
        self.check_for_collision_with_screen()
        return super().update()
    
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
        
        self.blue_entity = Entity(BLUE_IMG, center_x= 50, center_y=30)
        self.red_entity = Entity(RED_IMG, center_x= 150, center_y=130)

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        arcade.start_render()

        self.blue_entity.draw()
        self.red_entity.draw()

        arcade.finish_render()
        
    def update(self, delta_time):
        if arcade.check_for_collision(self.red_entity, self.blue_entity):
            print("Collision detected!")
        # self.blue_entity.move(1, 0)
        self.blue_entity.update()
        self.red_entity.update()

# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()
