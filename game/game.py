##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

import pygame as pg

from .constants import ASSETS, Colors
from .system.screen import BaseLayer, Screen

class MainMenuLayer(BaseLayer):
    def setup(self):
        def exit_main_menu(_):
            self.remove()
            return True

        self.when(pg.MOUSEBUTTONUP, exit_main_menu)

    def render(self):
        window = self.get_surface()
        window.fill(Colors.CYAN)
        window.blit(ASSETS.get("grandma").get_resource(),
            ((self.get_screen().width / 2) - 300,
             (self.get_screen().height / 2) - 200))

class Game:
    def __init__(self):
        self.screen = Screen()
        self.screen.add_layer(MainMenuLayer)

    def run(self):
        self.screen.start()
