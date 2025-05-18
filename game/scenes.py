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
            scale=3.0
        )
        self.add_animation("switch_between_frames", ObjectAnimator(
            setter=lambda frame, x, y: (
                self.set_state(frame),
                self.modify_pos(x, y)
            ),
            states=[
                (0, 0, 0, 0),
                (1, len(Cat.TILES), -100, -100)
            ],
            looping=True,
            duration=0.7,
            enabled=False
        ), GameObject.MODE_DELTA)

class ActionLayer(BaseLayer):
    cat = Cat()
    dish = Sprite(ASSETS, "plate")
    table = Sprite(ASSETS, "table", scale_to=(None, 1080))

    def setup(self):
        def mousemove(event):
            pos = pg.mouse.get_pos()
            self.cat.set_pos(*pos)
        self.when(pg.MOUSEMOTION, mousemove)

    def tick(self):
        screen = self.get_screen()
        time = float(screen.clock.get_time()) / 1000
        self.cat.animate_auto(time)

    def render(self):
        window = self.get_surface()
        self.table.render(window)
        self.cat.render(window)

class BackgroundLayer(BaseLayer):
    background = Sprite(ASSETS, "kitchen", scale_to=(None, 1080))
    grandma = Sprite(ASSETS, "grandma", scale=1.5, pos=(-100, 450))

    def setup(self):
        self.get_screen().add_layer(ActionLayer)
        self.grandma.add_animation("bouncy_ass_grandma", ObjectAnimator(
            setter=lambda y: (self.grandma.set_posy(y)),
            states=[
                (0, 450),
                (0.5, 490),
                (1, 450),
            ],
            looping=True,
            duration=50,
            curve=ObjectAnimator.EASE
        ), GameObject.MODE_DELTA)

    def tick(self):
        screen = self.get_screen()
        time = float(screen.clock.get_time()) / 1000
        self.grandma.animate_auto(time)
    
    def render(self):
        window = self.get_surface()
        window.fill(Colors.BLACK)
        self.background.render(window)
        self.grandma.render(window)
