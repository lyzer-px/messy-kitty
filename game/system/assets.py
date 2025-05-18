##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Asset classes
##

import pygame as pg

class AssetLoadingException(Exception): ...

class BaseAsset:
    resource = None

    def __init__(self, path: str):
        self.path = path

    def get_path(self):
        return self.path

    def get_resource(self):
        if self.resource is None:
            raise AssetLoadingException("Asset is not loaded")
        return self.resource

class Image(BaseAsset):
    def __init__(self, path: str):
        super(self.__class__, self).__init__(path)
        with open(path, "r") as file:
            self.resource = pg.image.load(file)

# TODO: Create Sound class

class AssetManager:
    def __init__(self, assets={}):
        self.assets = assets

    def get(self, key: str):
        return self.assets.get(key, None)
