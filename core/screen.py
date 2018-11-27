import logging

import cv2
import mss
import mss.tools
import numpy as np

from core.errors import ScreenshotError
from core.helpers.os_helpers import MONITORS

try:
    import Image
except ImportError:
    from PIL import Image

logger = logging.getLogger(__name__)


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


class Rectangle:
    """Rectangle class represents the coordinates and size of a region/screen."""

    def __init__(self, x_start: int = 0, y_start: int = 0, width: int = 0, height: int = 0):
        self.x = x_start
        self.y = y_start
        self.width: int = width
        self.height: int = height

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.x, self.y, self.width, self.height)


class Region(Rectangle):
    """Region is a rectangular area on a screen, which is defined by its upper left corner (x, y) as a distance relative
     to the upper left corner of the screen (0, 0) and its dimension (w, h) as its width and height.

     Coordinates are based on screen coordinates.

     origin                               top
        +-----> x increases                |
        |                           left  -+-  right
        v                                  |
     y increases                         bottom
     """

    def __init__(self, x_start: int = 0, y_start: int = 0, width=0, height=0):
        Rectangle.__init__(self, x_start, y_start, width, height)

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.x, self.y, self.width, self.height)

    def get_center(self) -> Location:
        """Returns a Location object for the center of te screen."""
        return Location(int((self.x + self.width) / 2), int((self.y + self.height) / 2))

    def move_to(self, location):
        """Set the position of this region regarding it's top left corner to the given location"""
        self.x = location.x
        self.y = location.y

    def get_top_left(self) -> Location:
        """Returns a Location object for the top left of te screen."""
        return Location(self.x, self.y)

    def get_top_right(self) -> Location:
        """Returns a Location object for the top right of te screen."""
        return Location(self.x + self.width, self.y)

    def get_bottom_left(self) -> Location:
        """Returns a Location object for the bottom left of te screen."""
        return Location(self.x, self.y + self.height)

    def get_bottom_right(self) -> Location:
        """Returns a Location object for the bottom right of te screen."""
        return Location(self.x + self.width, self.y + self.height)

    def get_region(self):
        """Returns a region."""
        return Region(self.x, self.y, self.width, self.height)

    def show(self):
        """Displays the screen region. This method is mainly intended for debugging purposes."""
        region = Rectangle(self.x, self.y, self.width, self.height)
        ScreenshotImage(region).image.show()

    def new_region(self, x_0: int, y_0: int, w: int, h: int):
        """Creates a new region from the current region."""
        if self.x + x_0 >= self.x and x_0 + w <= self.width and self.y + y_0 >= self.y and y_0 + h <= self.height:
            return Region(self.x + x_0, self.y + y_0, w, h)
        else:
            raise ValueError(
                'Out of bounds. Cannot create R1 %s in R2 %s' % (Region(self.x + x_0, self.y + y_0, w, h), self))


def _region_to_image(region) -> Image or ScreenshotError:
    try:
        image = np.array(mss.mss().grab(region))
        return Image.fromarray(image, mode='RGBA')
    except Exception:
        raise ScreenshotError('Unable to take screenshot.')


class Screen(Region):
    """Class Screen is the representation for a physical monitor where the capturing process (grabbing a rectangle
    from a screenshot). It is used for further processing with find operations. For Multi Monitor Environments it
    contains features to map to the relevant monitor.
    """

    def __init__(self, screen_id: int = 0):
        self.screen_id = screen_id
        self.screen_list = [item for item in MONITORS]
        self._bounds = _get_screen_details(self.screen_list, self.screen_id)
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


def _get_screen_details(screen_list: list, screen_id: int) -> Rectangle:
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
            return Rectangle(details['left'], details['top'], details['width'], details['height'])
        except IndexError:
            logger.warning('Screen %s does not exist. Available monitors: %s'
                           % (screen_id, ', '.join(_get_available_monitors(screen_list))))
    return Rectangle()


def _get_available_monitors(screen_list: list) -> list:
    """Return a list with all the available monitors."""
    res = []
    for screen in screen_list:
        res.append('Screen(%s)' % screen_list.index(screen))
    return res


class ScreenshotImage:
    """This class represents the visual representation of a region/screen."""

    def __init__(self, region: Rectangle = None, screen_id: int = 0):
        if region is None:
            region = Screen(screen_id).get_bounds()

        screen_region = {'top': region.y, 'left': region.x, 'width': region.width, 'height': region.height}

        self.image = _region_to_image(screen_region)
        self.rgb_array = np.array(self.image)
        self.gray_array = cv2.cvtColor(np.array(self.image), cv2.COLOR_BGR2GRAY)
        height, width = self.gray_array.shape
        self.width = width
        self.height = height

    def binarize(self):
        return cv2.threshold(self.gray_array, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


# region1 = Screen(0).new_region(0, 0, 50, 50)
# print(region1.get_region())
# print(region1.get_bottom_right())
# region1.show()
