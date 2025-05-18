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

class ActionLayer(BaseLayer):
    cat = Sprite(ASSETS, "cat")
    dish = Sprite(ASSETS, "dish")

    def setup(self):
        def mousemove(event):
            ...
        self.when(pg.MOUSEMOTION, mousemove)

    def tick(self):
        ...

    def render(self):
        ...

class BackgroundLayer(BaseLayer):
    background = Sprite(ASSETS, "kitchen")

    def setup(self):
        self.get_screen().add_layer(ActionLayer)
    
    def render(self):
        window = self.get_surface()
        window.fill(Colors.BLACK)
        self.background.render(window)
