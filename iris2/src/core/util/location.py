# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class Location:
    """Class handle single points on the screen directly by its position (x, y). It is mainly used in the actions on a
    region, to directly denote the click point. It contains methods, to move a point around on the screen."""

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.x, self.y)

    def offset(self, away_x: int, away_y: int):
        """Return a location object which is away_x and away_y pixels away horizontally and vertically from the current
        location.

        :param away_x: Offset added to location x parameter.
        :param away_y: Offset added to location y parameter.
        :return: Location object.
        """
        self.x += away_x
        self.y += away_y
        return self

    def above(self, away_y: int):
        """Return a location object which is away_y pixels vertically above the current location.

        :param away_y: Offset decreased from the location y parameter.
        :return: Location object.
        """
        self.y -= away_y
        return self

    def below(self, away_y: int):
        """Return a location object which is away_y pixels vertically below the current location.

        :param away_y: Offset added to location y parameter.
        :return: Location object.
        """
        self.y += away_y
        return self

    def left(self, away_x: int):
        """Return a location object which is away_x pixels horizontally to the left of the current location.

        :param away_x: Offset decreased from the location x parameter.
        :return: Location object.
        """
        self.x -= away_x
        return self

    def right(self, away_x: int):
        """Return a location object which is away_x pixels horizontally to the right of the current location.

        :param away_x: Offset added to location x parameter.
        :return: Location object.
        """
        self.x += away_x
        return self
