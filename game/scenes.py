##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Layer definitions
##

import pygame as pg
import random

from .constants import ASSETS, Colors
from .system.screen import BaseLayer, Screen
from .system.render import GameObject, ObjectAnimator, RectangularObject, Sprite

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
            scale=3
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

class Plate(Sprite):
    TILE_SIZE = (43, 17)
    TILES = [
        (0, 18),
        (0, 0),
    ]

    def __init__(self):
        super(Plate, self).__init__(
            ASSETS, "plate",
            states=Plate.TILES,
            tile_size=Plate.TILE_SIZE,
            scale=3
        )

class ActionLayer(BaseLayer):
    cat = Cat()
    plate = Plate()
    table = Sprite(ASSETS, "table", scale_to=(None, 1080))
    target = RectangularObject()
    drawer = RectangularObject()

    def setup(self):
        self.base_plate = (100, 640)
        self.max_plate_in_pile = 130
        self.plate_pile = [(40 + random.randint(0, 2), (1000 - (i * 10)),) for i in range(self.max_plate_in_pile)]
        self.plate_count = 20
        self.dragged_plate = False
        self.mouse_pos = (1920 / 2, 1080 / 2)
        self.plate_pos = (1920 / 2 + 100, 1080 / 2)
        self.target.set_size(1, 1);
        self.drawer.set_size(30, 30);
        self.drawer.set_pos(0, 0);

    def add_plate_to_pile(self):
        self.plate_count += 1

    def tick(self):
        screen = self.get_screen()
        time = float(screen.clock.get_time()) / 1000
        self.cat.animate_auto(time)
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_button_pressed = pg.mouse.get_pressed()
        self.target.set_pos(*self.mouse_pos)
        self.cat.set_size(40, 40)
        if self.mouse_button_pressed[0]:
            self.plate_pos = self.mouse_pos
            self.plate.pos = self.plate_pile[self.plate_count - 1]
            self.plate.set_size(30 * 3, 30)
            if not self.dragged_plate and self.target.collides(self.plate) \
                and self.plate_count > 0:
                self.plate_count -= 1
                self.dragged_plate = True
            elif self.target.collides(self.cat):
                self.dragged_plate = False
        elif self.dragged_plate:
            if self.target.collides(self.drawer):
                print("Put in drawer")
            else:
                self.plate_count += 1
            self.dragged_plate = False

    def render(self):
        window = self.get_surface()
        pg.draw.rect(window, (0, 255, 0), (self.plate_pile[0], (30, 30)))
        self.plate.pos = self.base_plate
        self.cat.render(window)
        self.table.render(window)
        self.plate.render(window)
        self.tick()
        for i in range(self.plate_count):
            self.plate.pos = self.plate_pile[i]
            self.plate.render(window)
        if self.dragged_plate:
            self.plate.pos = self.plate_pos
            self.plate.render(window)
        self.plate.pos = self.plate_pile

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
