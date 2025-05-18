##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Screen class definition.
##

import pygame as pg

class Screen:
    def __init__(self):
        self.width: int = 1920
        self.height: int = 1080
        self.window = pg.display.set_mode((self.width, self.height))
