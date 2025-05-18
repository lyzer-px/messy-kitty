##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

import pygame as pg

from .constants import Colors, Assets
from .screen import Screen

class Game:
    def __init__(self):
        self.screen = Screen()
        self.framerate: float = 60
        self.screen_width: int = self.screen.width
        self.screen_height: int = self.screen.height
        self.runs: bool = True
        self.clock = pg.time.Clock()
        with open(Assets.grandma_path, 'r') as file:
            self.grandma = pg.image.load(file);
        pg.init()

    def run(self):
        while self.runs:
            pg.display.update()
            self.screen.window.fill(Colors.cyan)
            self.screen.window.blit(self.grandma, ((self.screen.width / 2) - 300, (self.screen.height / 2) - 200))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.runs = False

            pg.display.flip()
            self.clock.tick(self.framerate)
