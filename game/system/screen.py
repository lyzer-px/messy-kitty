##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Screen class definition.
##

import inspect
import pygame as pg

from abc import ABC, abstractmethod
from typing import Any, Callable

class Screen:
    def __init__(self, width=1920, height=1080, framerate=60):
        self.runs = False
        self.framerate = framerate
        self.width = width
        self.height = height
        self.window = pg.display.set_mode(
            (self.width, self.height,)
        )
        self.layers: list[BaseLayer] = []

    def update_all_layers(self):
        for layer in enumerate(self.layers):
            layer[1].active_index = layer[0]

    def add_layer(self, layer, *context):
        if inspect.isclass(layer):
            layer = layer(context=context) 
        if not isinstance(layer, BaseLayer):
            raise TypeError("Attempted to add a non-layer to a Screen")
        layer.active_parent = self
        self.layers.append(layer)
        self.layers.sort(key=lambda x:x.z_index)
        self.update_all_layers()

    def remove_layer(self, layer):
        if isinstance(layer, BaseLayer):
            layer.active_parent = None
        if self.layers.index(layer) < 0:
            return
        used_layer = self.layers.pop(self.layers.index(layer))
        if self.runs:
            used_layer.teardown()
        self.update_all_layers()

    def clear_layers(self):
        if self.runs:
            for layer in self.layers:
                layer.teardown()
        self.layers = []

    def start(self):
        self.runs = True
        self.clock = pg.time.Clock()
        pg.init()
        for layer in self.layers: layer.setup(*layer.context)
        while self.runs:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.runs = False
                for layer in self.layers:
                    if layer.trigger_event(event):
                        break
            pg.display.flip()
            for layer in self.layers: layer.tick(*layer.context)
            for layer in self.layers: layer.render(*layer.context)
            pg.display.update()
            self.clock.tick(self.framerate)
            if (len(self.layers)):
                self.runs = False
        for layer in self.layers: layer.teardown(*layer.context)
    
    def stop(self):
        self.runs = False


class BaseLayer(ABC):
    z_index = 0
    active_index = 0
    context = []

    def __init__(self,
                 z_index=None,
                 *,
                 active_parent=None,
                 context=None):
        if z_index is not None:
            self.z_index = z_index
        if context is not None:
            self.context = context
        self.active_parent = active_parent
        self.events: dict[int, list[Callable]] = {}

    @abstractmethod
    def setup(self): pass

    @abstractmethod
    def tick(self): pass

    @abstractmethod
    def render(self): pass

    @abstractmethod
    def teardown(self): pass

    def remove(self):
        if type(self.active_parent) is Screen:
            self.active_parent.remove_layer(self.active_parent)

    def when(self, event_type, function: Callable[[pg.event.Event], Any]):
        if self.events.get(event_type, None) is None:
            self.events[event_type] = []
        self.events[event_type].append(function)

    def trigger_event(self, event: pg.event.Event) -> bool:
        interrupted = False

        if self.events.get(event.type, None) is None:
            return False
        for listener in self.events[event.type]:
            interrupted = (listener(event) == True) or interrupted
        return interrupted

    def is_last_layer(self) -> bool:
        if type(self.active_parent) is Screen:
            return self.active_index == len(self.active_parent.layers) - 1
        return False

    def get_screen(self) -> Screen:
        if type(self.active_parent) is Screen:
            return self.active_parent
        raise RuntimeError("This layer isn't bound to a screen")

    def get_index(self) -> int:
        if type(self.active_parent) is Screen:
            return self.active_index
        return -1
