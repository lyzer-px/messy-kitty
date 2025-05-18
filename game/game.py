##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

from .system.screen import Screen
from .scenes import BackgroundLayer

class Game:
    def __init__(self):
        self.screen = Screen()
        self.screen.add_layer(BackgroundLayer)

    def run(self):
        self.screen.start()
