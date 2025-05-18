##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Default values used within the program
## (colors, asset paths...)
##

import pygame as pg

from enum import Enum

from .system.assets import AssetManager, Image

class Colors:
    cyan = pg.Color(0, 255, 255)

class PossibleEvents(Enum):
    ...

ASSETS = AssetManager({
    "grandma": Image('assets/grandma.png'),
    #"plate": Image('assets/plate.png'),
    #"table": Image('assets/table.png'),
    #"shelves": Image('assets/shelves')
})
