# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class Rectangle:
    """Rectangle class represents the coordinates and size of a region/screen."""

    def __init__(self, x_start: int = 0, y_start: int = 0, width: int = 0, height: int = 0):
        self.x = x_start
        self.y = y_start
        self.width = width
        self.height = height

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.x, self.y, self.width, self.height)
