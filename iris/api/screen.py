# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from image_search import SCREEN_WIDTH, SCREEN_HEIGHT
from region import Region, get_region


# todo Refactor this
class Screen(object):
    def __init__(self, screen_id=0):
        self.id = screen_id

    def capture(self, *args):
        f_arg = args[0]

        if f_arg is None:
            return

        elif isinstance(f_arg, Region):
            return get_region(f_arg)

        elif len(args) is 4:
            return get_region((args[0], args[1], args[2], args[3]))

    def getNumberScreens(self):
        return 1

    def getBounds(self):
        dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)
        return dimensions


def get_screen():
    """Returns full screen Image."""
    return Region(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
