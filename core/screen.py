import logging

import cv2
import mss
import numpy as np
from pyautogui import screenshot

logger = logging.getLogger(__name__)
MONITORS = mss.mss().monitors[1:]


class Location:
    """Class handle single points on the screen directly by its position (x, y). It is mainly used in the actions on a
    region, to directly denote the click point. It contains methods, to move a point around on the screen."""

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

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


class Rectangle:
    def __init__(self, start_point: Location = Location(0, 0), width: int = 0, height: int = 0):
        self.start_point: Location = start_point
        self.width: int = width
        self.height: int = height

    def __str__(self):
        return '(%s, %s, %s)' % (self.start_point, self.width, self.height)

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__, self.start_point, self.width, self.height)


class Display:
    def __init__(self, screen_id=0):
        self._screen_id = screen_id
        self._screen_list = [item for item in MONITORS]
        self._bounds = get_screen_details(self._screen_list, self._screen_id)

    def __str__(self):
        return '(%s, %s, %s)' % (self._bounds.start_point, self._bounds.width, self._bounds.height)

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__, self._bounds.start_point, self._bounds.width,
                                   self._bounds.height)

    def get_number_screens(self):
        """Returns the number of screens."""
        return len(self._screen_list)

    def get_bounds(self):
        """Call the get_screen_details() method."""
        return self._bounds


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
            return Rectangle(Location(details['left'], details['top']), details['width'], details['height'])
        except IndexError:
            logger.warning('Screen %s does not exist. Available monitors: %s'
                           % (screen_id, ', '.join(get_available_monitors(screen_list))))
    return Rectangle()


def get_available_monitors(screen_list):
    """Return a list with all the available monitors."""
    res = []
    for screen in screen_list:
        res.append('Screen(%s)' % screen_list.index(screen))
    return res


class ScreenshotImage:
    def __init__(self, region: Rectangle = None):

        if region is None:
            region = Display().get_bounds()

        region_coordinates = (region.start_point.x, region.start_point.y, region.width, region.height)
        print(region_coordinates)
        screen_pil_image = screenshot(region=region_coordinates)
        height, width = self._gray_array.shape

        self._gray_array = cv2.cvtColor(np.array(screen_pil_image), cv2.COLOR_BGR2GRAY)
        self.width = width
        self.height = height

    @property
    def image_gray_array(self):
        return self._gray_array

    def binarize(self):
        return cv2.threshold(self._gray_array, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
