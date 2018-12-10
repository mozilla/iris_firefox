# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from core.enums import Alignment
from core.helpers.location import Location


class Rectangle:
    """Rectangle class represents the coordinates and size of a region/screen."""

    def __init__(self, x_start: int = 0, y_start: int = 0, width: int = 0, height: int = 0):
        self.x = x_start
        self.y = y_start
        self.width = width
        self.height = height

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.x, self.y, self.width, self.height)

    def apply_alignment(self, align: Alignment = Alignment.TOP_LEFT):
        """Returns rectangle location based on alignment.

        :param align: Alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: Location object.
        """
        if align is Alignment.CENTER:
            return Location(self.x + int(self.width / 2), self.y + int(self.height / 2))
        elif align is Alignment.TOP_RIGHT:
            return Location(self.x + self.width, self.y)
        elif align is Alignment.BOTTOM_LEFT:
            return Location(self.x, self.y + self.height)
        elif align is Alignment.TOP_RIGHT:
            return Location(self.x + self.width, self.y + self.height)
        else:
            return Location(self.x, self.y)
