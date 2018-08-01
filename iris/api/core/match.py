# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from location import Location
from region import Region


class Match(Region):
    def __init__(self, x, y, width, height, score):
        Region.__init__(self, x, y, width, height)
        self._width = width
        self._height = height
        self._score = score

    def get_target(self):
        return Location(self._x, self._y)

    def get_score(self):
        return self._score
