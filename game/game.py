##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

from .system.screen import Screen
from .scenes import BootLayer

class Game:
    def __init__(self):
        self.screen = Screen()
        self.screen.add_layer(BootLayer)

    def run(self):
        self.screen.start()
