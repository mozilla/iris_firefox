# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
from typing import List

import mss

from src.core.api.rectangle import Rectangle

MONITORS = mss.mss().monitors[1:]
logger = logging.getLogger(__name__)


class Display:
    def __init__(self, screen_id: int = 0):
        self.bounds = _get_screen_details(screen_id)
        self.scale = _get_scale(screen_id)

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.bounds.x, self.bounds.y, self.bounds.width,
                                       self.bounds.height)


def _get_screen_details(screen_id: int) -> Rectangle:
    """Get the screen details.

    :param screen_id: Screen ID.
    :return: Region object.
    """
    if len(MONITORS) == 0:
        logger.error('Could not retrieve list of available monitors.')
    else:
        try:
            details = MONITORS[screen_id]
            return Rectangle(details['left'], details['top'], details['width'], details['height'])
        except IndexError:
            logger.warning('Screen %s does not exist. Available monitors: %s'
                           % (screen_id, ', '.join(_get_available_monitors(MONITORS))))
    return Rectangle()


def _get_available_monitors(screen_list: List) -> List:
    """Return a list with all the available monitors."""
    res = []
    for screen in screen_list:
        res.append('Screen(%s)' % screen_list.index(screen))
    return res


def _get_display_collection():
    res = []
    for index, item in enumerate(MONITORS):
        res.append(Display(index))
    return res


def _get_scale(screen_id):
    try:
        display = MONITORS[screen_id]
        display_width = display['width']
        screenshot = mss.mss().grab(display)
        return screenshot.width / display_width
    except IndexError:
        return 1


DisplayCollection = _get_display_collection()
