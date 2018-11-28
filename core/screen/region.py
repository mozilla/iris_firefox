# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from core.errors import FindError
from core.helpers.location import Location
from core.helpers.rectangle import Rectangle
from core.image_search.finder import wait
from core.image_search.image_search import match_template


class Region:
    """Region is a rectangular area on a screen, which is defined by its upper left corner (x, y) as a distance relative
     to the upper left corner of the screen (0, 0) and its dimension (w, h) as its width and height.

     Coordinates are based on screen coordinates.

     origin                               top
        +-----> x increases                |
        |                           left  -+-  right
        v                                  |
     y increases                         bottom
     """

    def __init__(self, x_start: int = 0, y_start: int = 0, width=0, height=0):
        self._area: Rectangle = Rectangle(x_start, y_start, width, height)
        self.x = x_start
        self.y = y_start
        self.width = width
        self.height = height

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.x, self.y, self.width, self.height)

    def get_center(self) -> Location:
        """Returns a Location object for the center of te screen."""
        return Location(int((self.x + self.width) / 2), int((self.y + self.height) / 2))

    def move_to(self, location):
        """Set the position of this region regarding it's top left corner to the given location"""
        self.x = location.x
        self.y = location.y

    def get_top_left(self) -> Location:
        """Returns a Location object for the top left of te screen."""
        return Location(self.x, self.y)

    def get_top_right(self) -> Location:
        """Returns a Location object for the top right of te screen."""
        return Location(self.x + self.width, self.y)

    def get_bottom_left(self) -> Location:
        """Returns a Location object for the bottom left of te screen."""
        return Location(self.x, self.y + self.height)

    def get_bottom_right(self) -> Location:
        """Returns a Location object for the bottom right of te screen."""
        return Location(self.x + self.width, self.y + self.height)

    def get_region(self):
        """Returns a region."""
        return Region(self.x, self.y, self.width, self.height)

    def new_region(self, x_0: int, y_0: int, w: int, h: int):
        """Creates a new region from the current region."""
        if self.x + x_0 >= self.x and x_0 + w <= self.width and self.y + y_0 >= self.y and y_0 + h <= self.height:
            return Region(self.x + x_0, self.y + y_0, w, h)
        else:
            raise ValueError(
                'Out of bounds. Cannot create R1 %s in R2 %s' % (Region(self.x + x_0, self.y + y_0, w, h), self))

    def find(self, ps=None):
        """Look for a single match of a Pattern or image.

        :param ps: Pattern or String.
        :return: Call the find() method.
        """
        return match_template(ps, self)

    def wait(self, what=None, timeout=None) -> bool or FindError:
        """Wait for a Pattern or image to appear.

        :param what: String or Pattern.
        :param timeout: Number as maximum waiting time in seconds.
        :return: True or FineError Exception.
        """
        return wait(what, timeout, self)
