# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import cv2
import mss
import numpy as np
import logging

import pyautogui as pyautogui

from src.core.api.errors import ScreenshotError
from src.core.api.os_helpers import OSHelper
from src.core.api.screen.display import DisplayCollection
from src.core.api.rectangle import Rectangle

try:
    import Image
except ImportError:
    from PIL import Image

logger = logging.getLogger(__name__)


class ScreenshotImage:
    """This class represents the visual representation of a region/screen."""

    def __init__(self, region: Rectangle = None, screen_id: int = 0):
        if region is None:
            region = DisplayCollection[screen_id].bounds

        if not OSHelper.is_linux():
            screen_region = region
        else:
            screen_region = {'top': region.y, 'left': region.x, 'width': region.width, 'height': region.height}

        self._color_image = _region_to_image(screen_region)
        self._rgb_array = np.array(self._color_image)
        self._gray_image = self._color_image.convert('L')
        self._gray_array = np.array(self._gray_image)
        height, width = self._gray_array.shape
        self.width = width
        self.height = height

    def get_rgb_array(self):
        """Getter for the RGB array of image."""
        return self._rgb_array

    def get_color_image(self):
        """Getter for the color_image property."""
        return self._color_image

    def get_gray_image(self):
        """Getter for the gray_image property."""
        return self._gray_image

    def get_gray_array(self):
        """Getter for the gray_array property."""
        return self._gray_array

    def binarize(self):
        return cv2.threshold(self._gray_array, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


def _region_to_image(region) -> Image or ScreenshotError:
    if OSHelper.get_os().value == 'linux':
        grabbed_area = _mss_screenshot(region)
    else:
        try:
            grabbed_area = pyautogui.screenshot(region=(region.x, region.y, region.width, region.height))
        except (IOError, OSError):
            logger.debug('Call to pyautogui.screnshot failed, using mss instead.')
            grabbed_area = _mss_screenshot(region)
    return grabbed_area



def _mss_screenshot(region):
    try:
        image = np.array(mss.mss().grab(region))
    except Exception:
        raise ScreenshotError('Unable to take screenshot.')
    return Image.fromarray(image, mode='RGBA')
