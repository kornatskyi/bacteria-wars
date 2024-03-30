import arcade


class Environment:
    def __init__(self):
        self.herbivores = arcade.SpriteList()
        self.carnivores = arcade.SpriteList()
        self.plants = arcade.SpriteList()
