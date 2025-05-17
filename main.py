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


Cyan = (0, 255, 255)

class event:
    def __init__(self):
        self.event_total = 5
        self.event_prob = 1 # In percentage

class screen:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.window = pg.display.set_mode((self.screen.width, self.screen.height))
        background = pg.Rect(0, 0, self.width, self.height)

class game:
    def __init__(self):
        self.framerate = 60
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = screen()
        pg.init()
    def run(self):
        while True:
            pg.draw.rect(self.screen.background, Cyan, screen.window)




if __name__ == '__main__':
    game.run()