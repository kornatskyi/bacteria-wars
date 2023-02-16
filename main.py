# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Welcome to Arcade"
RADIUS = 10 
BLUE_IMG = "./blue.png"
RED_IMG = "./red.png"

class Entity(arcade.Sprite):
    def __init__(self, image, scale=0.1, border_color=arcade.color.BLACK, border_width=1):
        super().__init__(image, scale)
        self.border_color = border_color
        self.border_width = border_width

    def move(self, change_x, change_y):
        self.center_x += change_x
        self.center_y += change_y
    
    def draw(self):
        super().draw()
        # border
        arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height, self.border_color, self.border_width)
        # self.move(1, 1)

# Classes
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
        
        self.blue_entity = Entity(BLUE_IMG)
        self.red_entity = Entity(RED_IMG)

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        arcade.start_render()

        self.blue_entity.draw()
        self.red_entity.draw()
        # Draw a blue circle
        arcade.draw_circle_filled(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, RADIUS, arcade.color.BLUE
        )

# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()
