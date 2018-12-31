# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from core.errors import FindError
from core.finder.finder import verify, find, find_all, exists, highlight, wait_vanish
from core.helpers.location import Location
from core.helpers.rectangle import Rectangle
from core.mouse.mouse import move, press, release, click, right_click, double_click, drag_drop


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

    def __init__(self, x_start: int = 0, y_start: int = 0, width: int = 0, height: int = 0):
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
        return find(ps, self._area)

    def find_all(self, ps=None):
        """Look for multiple matches of a Pattern or image.

        :param ps: Pattern or String.
        :return: Call the find_all() method.
        """
        return find_all(ps, self._area)

    def wait(self, ps=None, timeout=None) -> bool or FindError:
        """Wait for a Pattern or image to appear.

        :param ps: Pattern or String.
        :param timeout: Number as maximum waiting time in seconds.
        :return: True or FineError Exception.
        """
        return verify(ps, timeout, self._area)

    def wait_vanish(self, ps=None, timeout=None) -> bool or FindError:
        """Wait for a Pattern or image to disappear.

        :param ps: Pattern or String.
        :param timeout: Number as maximum waiting time in seconds.
        :return: True or FineError Exception.
        """
        return wait_vanish(ps, timeout, self._area)

    def exists(self, ps=None, timeout=None):
        """Check if Pattern or image exists.

        :param ps: Pattern or String.
        :param timeout: Number as maximum waiting time in seconds.
        :return: Call the exists() method.
        """
        return exists(ps, timeout, self._area)

    def highlight(self, duration=None, color=None):
        """Region highlight.

        :param duration: How many seconds the region is highlighted. By default the region is highlighted for 2 seconds.
        :param color: Color used to highlight the region. Default color is red.
        :return: None.
        """
        highlight(self, duration, color)

    def mouse_move(self, ps=None, duration=None, align=None):
        """Mouse move.

        :param ps: Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return move(ps, duration, self._area, align)

    def mouse_press(self, ps=None, duration=None, button=None, align=None):
        """Mouse press.

        :param ps: Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param button: 'left','right' or 'middle'.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return press(ps, duration, self._area, button, align)

    def mouse_release(self, ps=None, duration=None, button=None, align=None):
        """Mouse release.

        :param ps: Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param button: 'left','right' or 'middle'.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return release(ps, duration, self._area, button, align)

    def click(self, ps=None, duration=None, align=None):
        """Mouse left click.

        :param ps: Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return click(ps, duration, self._area, align)

    def right_click(self, ps=None, duration=None, align=None):
        """Mouse right click.

        :param ps: Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return right_click(ps, duration, self._area, align)

    def double_click(self, ps=None, duration=None, align=None):
        """Mouse double click.

        :param ps: Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return double_click(ps, duration, self._area, align)

    def drag_drop(self, drag_from=None, drop_to=None, duration=None, align=None):
        """Mouse drag and drop.

        :param drag_from: Starting point for drag and drop. Can be pattern or String.
        :param drop_to: Ending point for drag and drop. Can be pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return drag_drop(drag_from, drop_to, self._area, duration, align)
