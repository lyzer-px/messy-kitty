#!/usr/bin/env python3
##
## EPITECH PROJECT, 2024
## messy-kitty
## File description:
## main.py
##

import pygame as pg
import random
import time

class Colors:
    def __init__(self):
        self.cyan = (0, 255, 255)

class Event:
    def __init__(self):
        self.event_total = 5
        self.event_prob = 1 # In percentage

class Screen:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.background = pg.Rect(0, 0, self.width, self.height)
        self.window = pg.display.set_mode((self.width, self.height))

class Game:
    def __init__(self):
        self.framerate = 60
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = Screen()
        self.colors = Colors()
        self.runs = True
        pg.init()
    def run(self):
        while self.run:
            pg.display.update()
            pg.draw.rect(self.screen.window, self.colors.cyan, self.screen.background)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False


if __name__ == '__main__':
    game = Game()
    game.run()