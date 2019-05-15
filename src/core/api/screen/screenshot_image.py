# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import cv2
import mss
import numpy as np
import logging

from pyautogui import screenshot

from src.core.api.errors import ScreenshotError
from src.core.api.os_helpers import OSHelper
from src.core.api.screen.display import DisplayCollection
from src.core.api.rectangle import Rectangle

try:
    import Image
except ImportError:
    from PIL import Image

logger = logging.getLogger(__name__)
_mss = mss.mss()


class ScreenshotImage:
    """This class represents the visual representation of a region/screen."""

    def __init__(self, region: Rectangle = None, screen_id: int = None):
        if screen_id is None:
            screen_id = 0

        if region is None:
            region = DisplayCollection[screen_id].bounds

        if OSHelper.is_linux():
            screen_region = region
        else:
            screen_region = {'top': int(region.y), 'left': int(region.x),
                             'width': int(region.width), 'height': int(region.height)}

        self._raw_image = _region_to_image(screen_region)
        self._gray_array = _convert_image_to_gray(self._raw_image)
        self._color_array=_convert_image_to_color(self._raw_image)


        height, width = self._gray_array.shape
        self.width = width
        self.height = height





        scale = DisplayCollection[screen_id].scale

        if scale != 1:
            self.width = int(width / scale)
            self.height = int(height / scale)
            self._color_array = cv2.resize(self._color_array,
                                          dsize=(self.width, self.height),
                                          interpolation=cv2.INTER_CUBIC)
            self._gray_array=cv2.resize(self._gray_array,
                                          dsize=(self.width, self.height),
                                          interpolation=cv2.INTER_CUBIC)


    def get_gray_array(self):
        """Getter for the gray_array property."""
        return self._gray_array

    def get_gray_image(self):
        """Getter for the gray_image property."""
        return Image.fromarray(self._gray_array)

    def binarize(self):
        return cv2.threshold(self._gray_array, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    def get_raw_image(self):
        """Getter raw_image property."""
        return Image.fromarray(self._raw_image)

    def get_raw_array(self):
        """Getter array property."""
        return self._raw_image

    def get_color_array(self):
        """Getter color array property."""
        return self._color_array

    def show_image(self):
        """Displays this image. This method is mainly intended for
        debugging purposes."""
        image = self.get_raw_image()
        return image.show()



def _region_to_image(region) -> Image or ScreenshotError:
    if not OSHelper.is_linux():
        grabbed_area = _mss_screenshot(region)
    else:
        try:
            grabbed_area = np.array(screenshot(region=(region.x, region.y, region.width, region.height)))
        except (IOError, OSError):
            logger.debug('Call to pyautogui.screnshot failed, using mss instead.')
            grabbed_area = _mss_screenshot(region)
    return grabbed_area


def _convert_image_to_gray(image):
    """Converts an Image to Gray
    :returns np array"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def _convert_image_to_color(image):
    """Converts an Image to Color
     :returns np array"""

    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


def _mss_screenshot(region):
    try:
        return np.array(_mss.grab(region))
    except Exception:
        raise ScreenshotError('Unable to take screenshot.')
