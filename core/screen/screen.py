# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging

from core.screen.region import Region
from core.helpers.rectangle import Rectangle
from core.screen.display import Display

logger = logging.getLogger(__name__)


class Screen(Region):
    """Class Screen is the representation for a physical monitor where the capturing process (grabbing a rectangle
    from a screenshot). It is used for further processing with find operations. For Multi Monitor Environments it
    contains features to map to the relevant monitor.
    """

    def __init__(self, screen_id: int = 0):
        self.screen_id = screen_id
        self.screen_list = Display(screen_id).screen_list
        self._bounds = Display(screen_id).bounds
        Region.__init__(self, self._bounds.x, self._bounds.y, self._bounds.width, self._bounds.height)

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self._bounds.x, self.y, self._bounds.width,
                                       self._bounds.height)

    def get_number_screens(self) -> int:
        """Get the number of screens in a multi-monitor environment at the time the script is running."""
        return len(self.screen_list)

    def get_bounds(self) -> Rectangle:
        """Get the dimensions of monitor represented by the screen object."""
        return self._bounds





# region1 = Screen(0).new_region(0, 0, 50, 50)
# print(region1.get_region())
# print(region1.get_bottom_right())
# region1.show()
