##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

import pygame as pg

from .system.assets import Assets
from .system.screen import Screen

class Game:
    def __init__(self):
        self.screen = Screen()

    def run(self):
        self.screen.start()
