# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

import mss
import pyautogui

from region import Region

logger = logging.getLogger(__name__)


class Screen(Region):
    def __init__(self, screen_id=0):
        """Function assign value to the '_screen_id' and '_screen_list' Screen parameters."""
        self._screen_id = screen_id
        self._screen_list = [item for item in mss.mss().monitors[1:]]
        Region.__init__(self, get_screen_details(self._screen_list, self._screen_id))

    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    screen_region = Region(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    TOP_HALF = Region.screen_regions(screen_region, 'TOP_HALF')
    BOTTOM_HALF = Region.screen_regions(screen_region, 'BOTTOM_HALF')

    LEFT_HALF = Region.screen_regions(screen_region, 'LEFT_HALF')
    RIGHT_HALF = Region.screen_regions(screen_region, 'RIGHT_HALF')

    TOP_THIRD = Region.screen_regions(screen_region, 'TOP_THIRD')
    MIDDLE_THIRD_HORIZONTAL = Region.screen_regions(screen_region, 'MIDDLE_THIRD_HORIZONTAL')
    BOTTOM_THIRD = Region.screen_regions(screen_region, 'BOTTOM_THIRD')

    LEFT_THIRD = Region.screen_regions(screen_region, 'LEFT_THIRD')
    MIDDLE_THIRD_VERTICAL = Region.screen_regions(screen_region, 'MIDDLE_THIRD_VERTICAL')
    RIGHT_THIRD = Region.screen_regions(screen_region, 'RIGHT_THIRD')

    UPPER_LEFT_CORNER = Region.screen_regions(screen_region, 'UPPER_LEFT_CORNER')
    UPPER_RIGHT_CORNER = Region.screen_regions(screen_region, 'UPPER_RIGHT_CORNER')
    LOWER_LEFT_CORNER = Region.screen_regions(screen_region, 'LOWER_LEFT_CORNER')
    LOWER_RIGHT_CORNER = Region.screen_regions(screen_region, 'LOWER_RIGHT_CORNER')

    def get_number_screens(self):
        """Returns the number of screens."""
        return len(self._screen_list)

    def get_bounds(self):
        """Call the get_screen_details() method."""
        return get_screen_details(self._screen_list, self._screen_id)


def get_screen_details(screen_list, screen_id):
    """Get the screen details.

    :param screen_list: List with available monitors.
    :param screen_id: Screen ID.
    :return: Region object.
    """
    if len(screen_list) == 0:
        logger.error('Could not retrieve list of available monitors.')
    else:
        try:
            details = screen_list[screen_id]
            return Region(details['left'], details['top'], details['width'], details['height'])
        except IndexError:
            logger.warning('Screen %s does not exist. Available monitors: %s'
                           % (screen_id, ', '.join(get_available_monitors(screen_list))))
    return Region()


def get_available_monitors(screen_list):
    """Return a list with all the available monitors."""
    res = []
    for screen in screen_list:
        res.append('Screen(%s)' % screen_list.index(screen))
    return res
