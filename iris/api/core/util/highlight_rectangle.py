# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.settings import Settings


class HighlightRectangle(object):
    def __init__(self, x, y, width, height, color=None, thickness=None):

        if thickness is None:
            thickness = Settings.highlight_thickness

        if color is None:
            color = Settings.highlight_color

        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
        self._thickness = thickness

    @property
    def x(self):
        """Getter for the x property."""
        return self._x

    @x.setter
    def x(self, x):
        """Setter for the x property."""
        self._x = x

    @property
    def y(self):
        """Getter for the y property."""
        return self._y

    @y.setter
    def y(self, y):
        """Getter for the y property."""
        self._y = y

    @property
    def width(self):
        """Getter for the width property."""
        return self._width

    @width.setter
    def width(self, width):
        """Setter for the width property."""
        self._width = width

    @property
    def height(self):
        """Getter for the height property."""
        return self._height

    @height.setter
    def height(self, height):
        """Setter for the height property."""
        self._height = height

    @property
    def color(self):
        """Getter for the color property."""
        return self._color

    @color.setter
    def color(self, color):
        """Setter for the color property."""
        self._color = color

    @property
    def thickness(self):
        """Getter for the thickness property."""
        return self._thickness

    @thickness.setter
    def thickness(self, thickness):
        """Setter for the thickness property."""
        self._thickness = thickness
