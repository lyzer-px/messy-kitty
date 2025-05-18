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

class Cat(Sprite):
    TILE_SIZE = (50, 50)
    TILES = [
        (12, 0),
        (9, 158),
        (64, 158),
        (119, 158),
        (173, 158),
        (173, 158),
    ]

    def __init__(self):
        super(Cat, self).__init__(
            ASSETS, "cat",
            states=Cat.TILES,
            tile_size=Cat.TILE_SIZE,
            scale=2.0
        )
        self.add_animation("switch_between_frames", ObjectAnimator(
            setter=lambda frame, x, y: (
                self.set_state(frame),
                self.set_pos(x, y)
            ),
            states=[
                (0, 0, 0, 0),
                (1, len(Cat.TILES), 100, 100)
            ],
            looping=True,
            duration=0.7
        ), GameObject.MODE_TIME)

class ActionLayer(BaseLayer):
    cat = Cat()
    dish = Sprite(ASSETS, "plate")
    table = Sprite(ASSETS, "table", scale_to=(None, 1080))

    def setup(self):
        def mousemove(event):
            ...
        self.when(pg.MOUSEMOTION, mousemove)

    def tick(self):
        ...

    def render(self):
        screen = self.get_screen()
        window = self.get_surface()
        time = float(screen.clock.get_time()) / 1000
        self.cat.render(window)
        self.cat.animate_auto(time)

class BackgroundLayer(BaseLayer):
    background = Sprite(ASSETS, "kitchen", scale_to=(None, 1080))

    def setup(self):
        self.get_screen().add_layer(ActionLayer)
    
    def render(self):
        window = self.get_surface()
        window.fill(Colors.BLACK)
        self.background.render(window)
