##
## Epitech Game Jam - May 2025
## Messy kitty
##
## Game class definition.
##

import math
import sys
import pygame as pg

from abc import ABC, abstractmethod
from typing import Callable, Tuple

from .assets import AssetManager

class ObjectAnimator():
    LINEAR = lambda d:d
    EASE = lambda d:-(math.cos(math.pi * d) - 1) / 2

    def __init__(self, *,
                 setter: Callable | None = None,
                 states: list[Tuple[float | None, ...]] | None = [],
                 start: Tuple[int | float, ...] | None = None,
                 end: Tuple[int | float, ...] | None = None,
                 delay: int | float = 0.0,
                 duration: int | float = 1.0,
                 curve: Callable[[float], float] = lambda x:x,
                 interpolation: bool = True,
                 enabled: bool = True,
                 looping: bool = False):
        self.setter = setter
        self.looping = looping
        self.curve = curve
        self.delay = delay
        self.duration = duration
        self.interpolation = interpolation
        self.enabled = enabled
        self._time = 0.0
        self._reset = 0.0
        locstates = []
        if states is not None:
            locstates = states
        elif start is not None and end is not None:
            locstates = [(0.0, *start), (1.0, *end)]
        else:
            locstates = []
        if len(locstates) < 2: 
            raise ValueError("Animation must have at least two states")
        locstates.sort(key=lambda x:x[0] if x[0] is not None else 0)
        self._states: list[list[float | None]] = [list(e) for e in locstates]
        for i in range(1, len(self._states[0])):
            self._interpolate_columns(i)
        self.states: list[list[float]] = [
            [x for x in e if x is not None] for e in self._states]
        print(self.states)

    def _interpolate_columns(self, col):
        valid_rows = [
            i for i in range(len(self._states))
            if self._states[i][col] is not None
        ]
        if len(valid_rows) == 0:
            for row in self._states: row[col] = 0
            return
        if len(valid_rows) == 1:
            for row in self._states: row[col] = self._states[valid_rows[0]][col]
            return
        def apply(start, end):
            for i in range(start + 1, end):
                cdelta = (self._states[i][0] - self._states[start][0]) \
                       / (self._states[end][0] - self._states[start][0])
                vdelta = self._states[start][col] \
                       + (self._states[end][col] - self._states[start][col]) * cdelta
                self._states[i][col] = vdelta
        for iend in range(1, len(valid_rows)):
            start = valid_rows[iend - 1]
            end = valid_rows[iend]
            apply(start, end)
        apply(-(len(self._states) - valid_rows[-1]), valid_rows[0])

    def push_state(self, time: float, values: Tuple[int | float]):
        self.states.append([time, *values])
        self.states.sort(key=lambda x:x[0])

    def reset_time_anim(self, seconds: float = 0.0):
        self._reset = seconds

    def reset_delta_anim(self, seconds: float = 0.0):
        self._time = seconds

    def enable(self): self.enabled = True
    def disable(self): self.enabled = False

    def animate_time(self, seconds: float):
        if not self.enabled: return
        if self.setter is not None:
            self.setter(*self.get_seconds_anim_values(seconds))
        else:
            raise ValueError("Setter not enabled, cannot use this method")

    def animate_delta(self, delta_seconds: float):
        if not self.enabled: return
        self._time += delta_seconds
        if self.setter is not None:
            self.setter(*self.get_seconds_anim_values(self._time))
        else:
            raise ValueError("Setter not enabled, cannot use this method")

    def animate_percent(self, cursor: float):
        if not self.enabled: return
        if self.setter is not None:
            self.setter(*self.get_anim_values(cursor))
        else:
            raise ValueError("Setter not enabled, cannot use this method")

    def get_seconds_anim_values(self, seconds: float) -> list[int | float]:
        seconds -= self._reset + self.delay
        return self.get_anim_values(seconds / self.duration)

    def get_anim_values(self, cursor: float) -> list[int | float]: 
        if len(self.states) < 2:
            raise ValueError("Animation must have at least two states")
        if self.looping and cursor > 1:
            cursor = (cursor % (1 + sys.float_info.epsilon))
        if cursor < 0: return list(self.states[0][1:])
        if cursor > 1: return list(self.states[-1][1:])
        sindex = 0
        for i, s in enumerate(self.states):
            if (cursor < s[0]): break
            sindex = i
        lo_state = self.states[sindex]
        if lo_state[0] > cursor or sindex + 1 >= len(self.states):
            return list(lo_state[1:])
        hi_state = self.states[sindex + 1]
        try:
            cdelta = (cursor - lo_state[0]) / (hi_state[0] - lo_state[0])
            cdelta = self.curve(cdelta)
            vdelta = [lo_state[i] + (hi_state[i] - lo_state[i]) * cdelta
                      for i in range(1, len(lo_state))]
            return vdelta if self.interpolation else list(lo_state[1:])
        except ZeroDivisionError:
            return list(hi_state[1:])

class GameObject(ABC):
    animators: dict[str, Tuple[str, ObjectAnimator]] = {}
    _last_time: float | None = None;

    MODE_TIME = "time"
    MODE_DELTA = "delta"

    def add_animation(self, name: str, anim: ObjectAnimator, mode: str):
        self.animators[name] = (mode, anim,)

    def get_animation(self, name: str) -> ObjectAnimator:
        return self.animators[name][1]

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
    def set_posx(self, x=0): self.set_pos(x, self._pos[1])
    def set_posy(self, y=0): self.set_pos(self._pos[0], y)

    def modify_pos(self, x=0, y=0):
        self._pos_mod = (x, y,)
        self.pos = (x + self._pos[0], y  + self._pos[1])
    def modify_posx(self, x=0): self.modify_pos(x, self._pos_mod[1])
    def modify_posy(self, y=0): self.modify_pos(self._pos_mod[0], y)

class SizableObject(GameObject):
    _size = (0, 0)
    _size_mod = (0, 0)
    size = (0, 0)

    def set_size(self, x=0, y=0):
        self._size = (x, y,)
        self.size = (x + self._size_mod[0], y  + self._size_mod[1])
    def set_sizex(self, x=0): self.set_size(x, self._size[1])
    def set_sizey(self, y=0): self.set_size(self._size[0], y)

    def modify_size(self, x=0, y=0):
        self._size_mod = (x, y,)
        self.size = (x + self._size[0], y  + self._size[1])
    def modify_sizex(self, x=0): self.modify_size(x, self._size_mod[1])
    def modify_sizey(self, y=0): self.modify_size(self._size_mod[0], y)

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
                 scale=1.0,
                 scale_to=(None, None),
                 states=None, tile_size=(16, 16)):
        self.images = []
        self.image = None
        self.pos = pos
        self.asset_name = asset_name
        self.asset = assets.get(asset_name or "default")
        self.state = 0
        self.scale = scale
        self.scale_to = scale_to
        sheet = self.asset.get_resource()
        if not isinstance(sheet, pg.Surface):
            raise TypeError("Wrong asset type for Sprite")
        if states is None:
            self.images = [sheet]
            self.set_state(0)
            return
        for e in states:
            self.images.append(
                sheet.subsurface(
                pg.rect.Rect(*([*e, *tile_size][:4]))
            ))
        self.set_state(0)

    def set_state(self, state: int):
        print(state)
        state = int(state)
        self.state = max(min(state, len(self.images) - 1), 0)
        image = self.images[self.state]
        rect = image.get_rect()
        nsz = (rect.width * self.scale, rect.height * self.scale)
        if self.scale_to[1] is not None:
            nsz = (nsz[0] * (self.scale_to[1] / nsz[1]), self.scale_to[1])
        elif self.scale_to[0] is not None:
            nsz = (self.scale_to[0], nsz[1] * (self.scale_to[0] / nsz[0]))
        self.set_size(int(nsz[0]), int(nsz[1]))
        self.image = pg.transform.scale(image, nsz)

    def next_state(self):
        self.set_state(self.state + 1 % len(self.images))

    def render(self, surface: pg.Surface):
        if self.image is not None:
            surface.blit(self.image, self.pos)
