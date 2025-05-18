##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

from .assets import AssetManager
import pygame as pg

class Sprite(pg.sprite.Sprite):
    def __init__(self, assets: AssetManager, list):
        super().__init__()
        self.images = {}
        if (len(list) == 0):
            return
        for i in range(len(list)):
            texture_name, coords = list[i]
            spritesheet = assets.get(texture_name)
            if (spritesheet is None):
                return
            self.images[str(i)] = spritesheet.spritesheet.subsurface(coords)
        self.set_state(0)

    def set_state(self, state: int):
        self.state = max(min(len(self.image), state), 0)
        self.image = self.images[self.state]

    def next_state(self):
        self.set_state(self.state + 1 % len(self.images))
