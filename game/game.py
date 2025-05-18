##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

import pygame as pg

from .constants import ASSETS
from .system.screen import BaseLayer, Screen

class MainMenuLayer(BaseLayer):
    def setup(self):
        def exit_main_menu(_):
            self.remove()
        self.when(pg.MOUSEBUTTONUP, exit_main_menu)

    def render(self):
        pass

class Game:
    def __init__(self):
        self.screen = Screen()
        self.screen.add_layer(MainMenuLayer)

    def run(self):
        self.screen.start()
