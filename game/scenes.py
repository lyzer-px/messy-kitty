##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Layer definitions
##

import pygame as pg

from .constants import ASSETS, Colors
from .system.screen import BaseLayer, Screen
from .system.render import GameObject, ObjectAnimator, RectangularObject, Sprite

class ActionLayer(BaseLayer):
    cat = Sprite(ASSETS, "cat")
    plate = Sprite(ASSETS, "plate")
    target = RectangularObject()
    drawer = RectangularObject()

    def setup(self):
        self.base_plate = (100, 640)
        plate_holder = pg.Rect(0, 0, 30, 30)
        self.max_plate_in_pile = 10
        self.plate_pile = [(1920 / 2, (640 + (i * 4)),) for i in range(self.max_plate_in_pile)]
        self.plate_count = 2
        self.dragged_plate = False
        self.mouse_pos = (1920 / 2, 1080 / 2)
        self.plate_pos = (1920 / 2 + 100, 1080 / 2)
        self.target.set_size(1, 1);
        self.drawer.set_size(30, 30);
        self.drawer.set_pos(0, 0);

    def add_plate_to_pile(self):
        self.plate_count += 1

    def tick(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_button_pressed = pg.mouse.get_pressed()
        self.target.set_pos(*self.mouse_pos)
        if self.mouse_button_pressed[0]:
            self.plate_pos = self.mouse_pos
            self.plate.pos = self.plate_pile[self.plate_count - 1]
            self.plate.set_size(30, 30)
            if not self.dragged_plate and self.target.collides(self.plate) \
                and self.plate_count > 0:
                self.plate_count -= 1
                self.dragged_plate = True
            elif self.target.collides(self.cat):
                self.dragged_plate = False
        elif self.dragged_plate:
            print(self.drawer.size, self.drawer.pos, self.target.size, self.target.pos)
            if self.target.collides(self.drawer):
                print("Put in drawer")
            else:
                self.plate_count += 1
            self.dragged_plate = False

    def render(self):
        window = self.get_surface()
        pg.draw.rect(window, (0, 255, 0), (self.plate_pile[0], (30, 30)))
        self.plate.pos = self.base_plate
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
    background = Sprite(ASSETS, "kitchen")

    def setup(self):
        self.get_screen().add_layer(ActionLayer)
    def render(self):
        window = self.get_surface()
        window.fill(Colors.BLACK)
        self.background.render(window)
