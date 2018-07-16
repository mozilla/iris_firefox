# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from util.core_helper import INVALID_NUMERIC_INPUT


class Location(object):
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if isinstance(x, int):
            self._x = x
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if isinstance(y, int):
            self._y = y
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    def set_location(self, x=0, y=0):
        self._x = x
        self._y = y

    def offset(self, away_x, away_y):
        new_x = int(self._x + away_x)
        new_y = int(self._y + away_y)
        return Location(new_x, new_y)

    def above(self, away_y):
        new_y = int(self._y - away_y)
        return Location(self._x, new_y)

    def below(self, away_y):
        new_y = int(self._y + away_y)
        return Location(new_y)

    def left(self, away_x):
        new_x = int(self._x - away_x)
        return Location(new_x, self.y)

    def right(self, away_x):
        new_x = int(self._x + away_x)
        return Location(new_x, self.y)
