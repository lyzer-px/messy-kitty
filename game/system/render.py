##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

import sys
import pygame as pg

from abc import ABC, abstractmethod
from typing import Callable, Tuple

from .assets import AssetManager

class ObjectAnimator():
    def __init__(self, *,
                 setter: Callable[[int | float], None] | None = None,
                 states: list[Tuple[float, int | float]] | None = [],
                 start: int | float | None = None,
                 end: int | float | None = None,
                 delay: int | float = 0.0,
                 duration: int | float = 1.0,
                 curve: Callable[[float], float] = lambda x:x,
                 looping: bool = False):
        self.setter = setter
        self.looping = looping
        self.curve = curve
        self.delay = delay
        self.duration = duration
        self._time = 0.0
        self._reset = 0.0
        if states is not None:
            self.states = states
        elif start is not None and end is not None:
            self.states = [(0.0, start), (1.0, end)]
        else:
            self.states = []
        self.states.sort(key=lambda x:x[0])

    def push_state(self, time: float, value: int | float):
        self.states.append((time, value,))
        self.states.sort(key=lambda x:x[0])

    def reset_time_anim(self, seconds: float = 0.0):
        self._reset = seconds

    def reset_delta_anim(self, seconds: float = 0.0):
        self._time = seconds

    def animate_time(self, seconds: float):
        if self.setter is not None:
            self.setter(self.get_seconds_anim_value(seconds))
        else:
            raise ValueError("Setter not enabled, cannot use this method")

    def animate_delta(self, delta_seconds: float):
        self._time += delta_seconds
        if self.setter is not None:
            self.setter(self.get_seconds_anim_value(self._time))
        else:
            raise ValueError("Setter not enabled, cannot use this method")

    def animate_percent(self, cursor: float):
        if self.setter is not None:
            self.setter(self.get_anim_value(cursor))
        else:
            raise ValueError("Setter not enabled, cannot use this method")

    def get_seconds_anim_value(self, seconds: float) -> int | float:
        seconds -= self._reset + self.delay
        return self.get_anim_value(seconds / self.duration)

    def get_anim_value(self, cursor: float) -> int | float: 
        if len(self.states) < 2:
            raise ValueError("Animation must have at least two states")
        if self.looping and cursor > 1:
            cursor = (cursor % (1 + sys.float_info.epsilon))
        if cursor < 0: return self.states[0][1]
        if cursor > 1: return self.states[-1][1]
        cursor = self.curve(cursor)
        sindex = 0
        for i, s in enumerate(self.states[1:]):
            if (s[0] > cursor): break
            sindex = i
        lo_state = self.states[sindex]
        if lo_state[0] > cursor or len(self.states) <= sindex + 1:
            return lo_state[1]
        hi_state = self.states[sindex + 1]
        try:
            cdelta = (cursor - lo_state[0]) / (hi_state[0] - lo_state[0])
            return lo_state[1] + (hi_state[1] - lo_state[1]) * cdelta
        except ZeroDivisionError:
            return hi_state[1]

class GameObject(ABC):
    animators: dict[str, Tuple[str, ObjectAnimator]] = {}
    _last_time: float | None = None;

    MODE_TIME = "time"
    MODE_DELTA = "delta"

    def add_animation(self, name: str, anim: ObjectAnimator, mode: str):
        self.animators[name] = (mode, anim,)

    def del_animation(self, name, *, reset: bool=False):
        setter = self.animators[name][1].setter
        if reset and setter is not None:
            setter(0)
        self.animators.pop(name)

    def animate_auto(self, time: float):
        if self._last_time is None:
            self._last_time = time
        self.animate_time(time)
        self.animate_delta(self._last_time - time)
        self._last_time = time

    def animate_time(self, delta_time: float, *, ignore_mode: bool=False):
        for mode, anim in self.animators.values():
            if ignore_mode or mode == GameObject.MODE_TIME:
                anim.animate_delta(delta_time)

    def animate_delta(self, delta_time: float, *, ignore_mode: bool=False):
        for mode, anim in self.animators.values():
            if ignore_mode or mode == GameObject.MODE_DELTA:
                anim.animate_delta(delta_time)

class StatefulObject(GameObject):
    state = 0

    @abstractmethod
    def set_state(self, state):...

    @abstractmethod
    def next_state(self):...

class PositionedObject(GameObject):
    _pos = (0, 0)
    _pos_mod = (0, 0)
    pos = (0, 0)

    def set_pos(self, x=0, y=0):
        self._pos = (x, y,)
        self.pos = (x + self._pos_mod[0], y  + self._pos_mod[1])

    def modify_pos(self, x=0, y=0):
        self._pos_mod = (x, y,)
        self.pos = (x + self._pos[0], y  + self._pos[1])

class SizableObject(GameObject):
    _size = (0, 0)
    _size_mod = (0, 0)
    size = (0, 0)

    def set_size(self, x=0, y=0):
        self._size = (x, y,)
        self.size = (x + self._size_mod[0], y  + self._size_mod[1])

    def modify_size(self, x=0, y=0):
        self._size_mod = (x, y,)
        self.size = (x + self._size[0], y  + self._size[1])

class RectangularObject(PositionedObject, SizableObject):
    def collides(self, other=None):
        if other is None:
            return False
        elif isinstance(other, RectangularObject):
            return self.size[0] + self.pos[0] > other.pos[0] \
               and self.size[1] + self.pos[1] > other.pos[1] \
               and self.pos[0] < other.pos[0] + other.pos[0] \
               and self.pos[1] < other.pos[1] + other.pos[1]
        elif type(other) is list:
            return any(self.collides(item) for item in other)
        return False

class RenderableObject(ABC):
    @abstractmethod
    def render(self, surface: pg.Surface): pass

class Sprite(StatefulObject, RectangularObject, RenderableObject):
    pos = (0, 0)

    def __init__(self,
                 assets: AssetManager,
                 asset_name=None,
                 pos=(0, 0),
                 *,
                 states=None, tile_size=(16, 16)):
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
        self.set_state(0)

    def set_state(self, state: int):
        self.state = max(min(state, len(self.images) - 1), 0)
        self.image = self.images[self.state]

    def next_state(self):
        self.set_state(self.state + 1 % len(self.images))

    def render(self, surface: pg.Surface):
        surface.blit(self.images[self.state], self.pos)
