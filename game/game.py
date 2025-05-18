##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

import pygame as pg

from .constants import ASSETS, Colors
from .system.screen import BaseLayer, Screen
from .system.render import GameObject, ObjectAnimator, Sprite

class MainMenuLayer(BaseLayer):
    grandma = Sprite(ASSETS, "grandma")

    def setup(self):
        def exit_main_menu(_):
            self.remove()
            return True
        self.when(pg.MOUSEBUTTONUP, exit_main_menu)

        self.grandma.add_animation("spin_grandma", ObjectAnimator(
            setter=lambda x, y: [
                self.grandma.set_pos(int(x), int(y)),
                self.grandma.set_pos(int(x), int(y))
            ],
            curve=ObjectAnimator.EASE,
            states=[
                (0.0, 0, 0, 0),
                (0.5, None, 600, 3),
                (1.0, 300, 600, 3)
            ],
            duration=1,
        ), GameObject.MODE_DELTA)
        self.grandma.get_animation("spin_grandma").reset_delta_anim();

    def render(self):
        screen = self.get_screen()
        time = float(screen.clock.get_time()) / 1000.0
        window = self.get_surface()
        window.fill(Colors.CYAN)
        self.grandma.animate_time(time)
        self.grandma.render(window)

class Game:
    def __init__(self):
        self.screen = Screen()
        self.screen.add_layer(MainMenuLayer)

    def run(self):
        self.screen.start()
