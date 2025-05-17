#!/usr/bin/env python3
##
## EPITECH PROJECT, 2024
## messy-kitty
## File description:
## main.py
##

import pygame as pg

class event:
    def __init__(self):
        self.event_total = 5

class game:
    def __init__(self):
        self.event_prob = 1 # In percentage
    def run(self):
        pg.init()
        pg.display.set_mode((1920, 1080))


if __name__ == '__main__':
    game.run()