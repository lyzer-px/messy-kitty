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
    plate = Sprite(ASSETS, "plate")

    def setup(self):
        self.base_plate = (100, 640)
        plate_holder = pg.Rect(0, 0, 30, 30)
        self.max_plate_in_pile = 10
        self.plate_pile = [(1920 / 2, (640 + (i * 4)),) for i in range(self.max_plate_in_pile)]
        self.plate_count = 0
        self.mouse_pos = (1920 / 2, 1080 / 2)
        self.plate_pos = (1920 / 2 + 100, 1080 / 2)
        pg.mouse.set_pos(self.mouse_pos)
        def add_plate_to_pile(self):
            self.plate_count += 1
        def plate_move(event):
            self.mouse_pos = pg.mouse.get_pos()
            self.mouse_button_pressed = pg.mouse.get_pressed()
            if self.mouse_button_pressed[0] and self.mouse_pos == self.base_plate:
                if event.button == 1:
                    self.plate_pos = self.mouse_pos
            if event.type == pg.KEYUP and event.key == pg.K_LEFT and self.plate_holder.collidepoint(self.mouse_pos):
                add_plate_to_pile()
                print(self.plate_count)
        self.when(pg.MOUSEMOTION, plate_move)

    def render(self):
        window = self.get_surface()
        pg.draw.rect(window, (0, 255, 0), (self.plate_pile[0], (30, 30)))
        self.plate.pos = self.base_plate
        self.plate.render(window)
        self.tick()
        for i in range(self.plate_count):
            self.plate.pos = self.plate_pile[i]
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
