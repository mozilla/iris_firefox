# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.settings import Settings


class HighlightCircle(object):
    def __init__(self, center_x, center_y, radius, color=None, thickness=None):

        if thickness is None:
            thickness = Settings.highlight_thickness

        if color is None:
            color = Settings.highlight_color

        self._center_x = center_x
        self._center_y = center_y
        self._radius = radius
        self._color = color
        self._thickness = thickness

    @property
    def center_x(self):
        return self._center_x

    @center_x.setter
    def center_x(self, center_x):
        self._center_x = center_x

    @property
    def center_y(self):
        return self._center_y

    @center_y.setter
    def center_y(self, center_y):
        self._center_y = center_y

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, thickness):
        self._thickness = thickness
