import pygame as pg

class Image:
    def __init__(self, path: str):
        self.path = path
        self.resource = pg.image.load(path)

    def get_path(self):
        return self.path

    def get_resource(self):
        return self.resource

class Sound:
    def __init__(self, path: str):
        self.path = path
        self.resource = pg.image.load(path)

    def get_path(self):
        return self.path

    def get_resource(self):
        return self.resource



class Assets:
    def __init__(self):
        self.registry = {
            'grandma': Image('assets/grandma.png'),
            'table': Image('assets/table.png'),
            'shelves': Image('assets/shelves')
        }

    def get(self, key: str):
        return self.registry[key]
