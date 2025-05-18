##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Layer definitions
##

import pygame as pg

from .constants import ASSETS, Colors
from .system.screen import BaseLayer, Screen
from .system.render import GameObject, ObjectAnimator, Sprite

class MainMenuLayer(BaseLayer):
    def setup(self):
        def exit_main_menu(_):
            self.remove()
            return True
        self.when(pg.MOUSEBUTTONUP, exit_main_menu)

    def render(self):
        screen = self.get_screen()
        window = self.get_surface()
        window.fill(Colors.CYAN)

class BootLayer(BaseLayer):
    def setup(self):
        self.get_screen().add_layer(MainMenuLayer)
        self.remove()
