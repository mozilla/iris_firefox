# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from src.core.api.errors import FindError
from src.core.api.finder.finder import wait, find, find_all, exists, highlight, wait_vanish
from src.core.api.location import Location
from src.core.api.mouse.mouse import move, press, release, click, right_click, double_click, drag_drop, hover
from src.core.api.rectangle import Rectangle


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
        self._area = Rectangle(x_start, y_start, width, height)
        self.x = x_start
        self.y = y_start
        self.width = width
        self.height = height

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.x, self.y, self.width, self.height)

    def top_half(self):
        return Region.screen_regions(self, 'TOP_HALF')

    def bottom_half(self):
        return Region.screen_regions(self, 'BOTTOM_HALF')

    def left_half(self):
        return Region.screen_regions(self, 'LEFT_HALF')

    def right_half(self):
        return Region.screen_regions(self, 'RIGHT_HALF')

    def top_third(self):
        return Region.screen_regions(self, 'TOP_THIRD')

    def middle_third_horizontal(self):
        return Region.screen_regions(self, 'MIDDLE_THIRD_HORIZONTAL')

    def bottom_third(self):
        return Region.screen_regions(self, 'BOTTOM_THIRD')

    def left_third(self):
        return Region.screen_regions(self, 'LEFT_THIRD')

    def middle_third_vertical(self):
        return Region.screen_regions(self, 'MIDDLE_THIRD_VERTICAL')

    def right_third(self):
        return Region.screen_regions(self, 'RIGHT_THIRD')

    def upper_left_corner(self):
        return Region.screen_regions(self, 'UPPER_LEFT_CORNER')

    def upper_right_corner(self):
        return Region.screen_regions(self, 'UPPER_RIGHT_CORNER')

    def lower_left_corner(self):
        return Region.screen_regions(self, 'LOWER_LEFT_CORNER')

    def lower_right_corner(self):
        return Region.screen_regions(self, 'LOWER_RIGHT_CORNER')

    def get_center(self) -> Location:
        """Returns a Location object for the center of te screen."""
        return Location(int((self.x + self.width) / 2), int((self.y + self.height) / 2))

    def move_to(self, location):
        """Set the position of this region regarding it's top left corner to the given location"""
        self.x = location.x
        self.y = location.y

    def get_top_left_coordinates(self) -> Location:
        """Returns a Location object for the top left of te screen."""
        return Location(self.x, self.y)

    def get_top_right_coordinates(self) -> Location:
        """Returns a Location object for the top right of te screen."""
        return Location(self.x + self.width, self.y)

    def get_bottom_left_coordinates(self) -> Location:
        """Returns a Location object for the bottom left of te screen."""
        return Location(self.x, self.y + self.height)

    def get_bottom_right_coordinates(self) -> Location:
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

    def hover(self, lps=None, align=None):
        """Mouse hover.

        :param lps: Location or Pattern or String.
        :param align: Hover location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        """
        return hover(lps, self._area, align)

    def wait(self, ps=None, timeout=None) -> bool or FindError:
        """Wait for a Pattern or image to appear.

        :param ps: Pattern or String.
        :param timeout: Number as maximum waiting time in seconds.
        :return: True or FineError Exception.
        """
        return wait(ps, timeout, self._area)

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

    def mouse_move(self, lps=None, duration=None, align=None):
        """Mouse move.

        :param lps: Location, Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return move(lps, duration, self._area, align)

    def mouse_press(self, lps=None, duration=None, button=None, align=None):
        """Mouse press.

        :param lps: Location, Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param button: 'left','right' or 'middle'.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return press(lps, duration, self._area, button, align)

    def mouse_release(self, lps=None, duration=None, button=None, align=None):
        """Mouse release.

        :param lps: Location, Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param button: 'left','right' or 'middle'.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return release(lps, duration, self._area, button, align)

    def click(self, lps=None, duration=None, align=None):
        """Mouse left click.

        :param lps: Location, Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return click(lps, duration, self._area, align)

    def right_click(self, lps=None, duration=None, align=None):
        """Mouse right click.

        :param lps: Location, Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return right_click(lps, duration, self._area, align)

    def double_click(self, lps=None, duration=None, align=None):
        """Mouse double click.

        :param lps: Location, Pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return double_click(lps, duration, self._area, align)

    def drag_drop(self, drag_from=None, drop_to=None, duration=None, align=None):
        """Mouse drag and drop.

        :param drag_from: Starting point for drag and drop. Can be Location, pattern or String.
        :param drop_to: Ending point for drag and drop. Can be pattern or String.
        :param duration: Speed of hovering from current location to target.
        :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
        :return: None.
        """
        return drag_drop(drag_from, drop_to, self._area, duration, align)

    @staticmethod
    def get_matrix(number_of_columns, number_of_lines, in_region=None):
        """Returns a "matrix" object(a list of lists) containing new Region objects representing that Region's
        subdivisions."""

        list_of_lists = []
        regions = []

        start_x = in_region.x
        start_y = in_region.y
        width = in_region.width
        height = in_region.height

        sub_region_width = width / number_of_columns
        sub_region_height = height / number_of_lines

        for i in range(number_of_lines):
            for j in range(number_of_columns):
                sub_region_x = (j * sub_region_width) + start_x
                sub_region_y = (i * sub_region_height) + start_y
                regions.append(Region(sub_region_x, sub_region_y, sub_region_width, sub_region_height))

            list_of_lists.append(regions)
            regions = []

        return list_of_lists

    @staticmethod
    def screen_regions(region, caption):
        captions = {
            'TOP_HALF': Region.get_matrix(1, 2, region)[0][0],
            'BOTTOM_HALF': Region.get_matrix(1, 2, region)[1][0],

            'LEFT_HALF': Region.get_matrix(2, 1, region)[0][0],
            'RIGHT_HALF': Region.get_matrix(2, 1, region)[0][1],

            'TOP_THIRD': Region.get_matrix(1, 3, region)[0][0],
            'MIDDLE_THIRD_HORIZONTAL': Region.get_matrix(1, 3, region)[1][0],
            'BOTTOM_THIRD': Region.get_matrix(1, 3, region)[2][0],

            'LEFT_THIRD': Region.get_matrix(3, 1, region)[0][0],
            'MIDDLE_THIRD_VERTICAL': Region.get_matrix(3, 1, region)[0][1],
            'RIGHT_THIRD': Region.get_matrix(3, 1, region)[0][2],

            'UPPER_LEFT_CORNER': Region.get_matrix(2, 2, region)[0][0],
            'UPPER_RIGHT_CORNER': Region.get_matrix(2, 2, region)[0][1],
            'LOWER_LEFT_CORNER': Region.get_matrix(2, 2, region)[1][0],
            'LOWER_RIGHT_CORNER': Region.get_matrix(2, 2, region)[1][1],
        }
        return captions.get(caption)
