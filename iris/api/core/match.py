# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from location import Location
from region import Region


class Match(Region):
    """An object of class Match represents the result of a successful find operation."""

    def __init__(self, x, y, width, height, score):
        """Function assign values to the x, y, width, height and score region parameters.

        :param x: Location x parameter.
        :param y: Location y parameter.
        :param width: Region's width.
        :param height: Region's height.
        :param score: Similarity with which the pattern is found.
        """

        Region.__init__(self, x, y, width, height)
        self.width = width
        self.height = height
        self.score = score

    def get_target(self):
        """Returns the location object that will be used as the click point."""
        return Location(self.x, self.y)

    def get_score(self):
        """Get the similarity score the image or pattern was found. The value is between 0 and 1."""
        return self.score
