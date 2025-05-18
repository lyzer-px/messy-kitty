#!/usr/bin/env python3
##
## EPITECH PROJECT, 2024
## messy-kitty
## File description:
## main.py
##

import assets
import pygame as pg
import random
import time


class Colors:
    def __init__(self):
        self.cyan = (0, 255, 255)

class Event:
    def __init__(self):
        self.event_total: int = 5
        self.event_prob: float = 1 # In percentage

class Screen:
    def __init__(self):
        self.width: int = 1920
        self.height: int = 1080
        self.window = pg.display.set_mode((self.width, self.height))

class Game:
    def __init__(self):
        self.screen = Screen()
        self.framerate: float = 60
        self.screen_width: int = self.screen.width
        self.screen_height: int = self.screen.height
        self.colors = Colors()
        self.assets = assets.Assets()
        self.runs: bool = True
        self.clock = pg.time.Clock()
        # self.grandma = pg.image.load(self.assets.)
        pg.init()

    def run(self):
        while self.runs:
            pg.display.update()
            self.screen.window.fill(self.colors.cyan)
            self.screen.window.blit(self.assets.get('grandma'), ((self.screen.width / 2) - 300, (self.screen.height / 2) - 200))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.runs = False

            pg.display.flip()
            self.clock.tick(self.framerate)



if __name__ == '__main__':
    game = Game()
    game.run()
