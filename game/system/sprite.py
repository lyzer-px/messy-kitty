##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

from .assets import AssetManager
import pygame as pg

class Sprite(pg.sprite.Sprite):
    pos = (0, 0)

    def __init__(self,
                 assets: AssetManager,
                 asset_name=None,
                 pos=(0, 0),
                 *,
                 states=None, tile_size=(16, 16)):
        super().__init__()
        self.images = []
        self.pos = pos
        self.asset_name = asset_name
        self.asset = assets.get(asset_name or "default")
        self.state = 0
        sheet = self.asset.get_resource()
        if not isinstance(sheet, pg.Surface):
            raise TypeError("Wrong asset type for Sprite")
        if states is None:
            self.images = [sheet]
            return
        for e in states:
            self.images.append(sheet.subsurface(
                pg.rect.Rect(*([*e, *tile_size][:4]))
            ))

    def set_state(self, state: int):
        self.state = max(min(len(self.images), state), 0)
        self.image = self.images[self.state]

    def next_state(self):
        self.set_state(self.state + 1 % len(self.images))

    def render(self, sf: pg.Surface):
        sf.blit(self.images[self.state], self.pos)
