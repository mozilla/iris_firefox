import logging
import os

import cv2
import numpy as np

try:
    import Image
except ImportError:
    from PIL import Image

FIND_METHOD = cv2.TM_CCOEFF_NORMED

logger = logging.getLogger(__name__)


def _parse_name(full_name):
    """Detects scale factor in image name

    :param str full_name: Image full name. Valid format name@[scale_factor]x.png.
    Examples: google_search@2x.png, amazon_logo@2.5x.png

    :return: Pair of image name and scale factor.
    """
    start_symbol = '@'
    end_symbol = 'x.'
    if start_symbol not in full_name:
        return full_name, 1
    else:
        try:
            start_index = full_name.index(start_symbol)
            end_index = full_name.index(end_symbol, start_index)
            scale_factor = float(full_name[start_index + 1:end_index])
            image_name = full_name[0:start_index] + full_name[end_index + 1:len(full_name)]
            return image_name, scale_factor

        except ValueError:
            logger.warning('Invalid file name format: "%s".' % full_name)
            return full_name, 1


def _apply_scale(scale, rgb_array):
    """Resize the image for HD images

    :param scale: scale of image
    :param rgb_array: rgb array of image
    :return: Scaled image
    """
    if scale > 1:
        temp_h, temp_w, not_needed = rgb_array.shape
        new_w, new_h = int(temp_w / scale), int(temp_h / scale)
        return cv2.resize(rgb_array, (new_w, new_h), interpolation=cv2.INTER_AREA)
    else:
        return rgb_array


def iris_image_match_template(needle, haystack, precision, threshold=None):
    """Finds a match or a list of matches

    :param needle:  Image details (needle)
    :param haystack: Region as Image (haystack)
    :param float precision: Min allowed similarity
    :param float || None threshold:  Max threshold
    :return: A location or a list of locations
    """
    is_multiple = threshold is not None

    from iris.api.core import Location
    try:
        res = cv2.matchTemplate(np.array(needle), np.array(haystack), FIND_METHOD)
    except:
        res = Location(-1, -1)

    if not is_multiple:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return Location(-1, -1)
        else:
            position = Location(max_loc[0], max_loc[1])
            return position
    else:
        if precision > threshold:
            precision = threshold

        w, h = needle.shape[::-1]
        points = []
        while True:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if FIND_METHOD in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc

            if threshold > max_val > precision:
                sx, sy = top_left
                for x in range(sx - w / 2, sx + w / 2):
                    for y in range(sy - h / 2, sy + h / 2):
                        try:
                            res[y][x] = np.float32(-10000)
                        except IndexError:
                            pass
                new_match_point = Location(top_left[0], top_left[1])
                points.append(new_match_point)
            else:
                break


class IrisImage:
    def __init__(self, file_name=None, dir_name=None):
            name, factor = _parse_name(file_name)
            self._name = name
            self._path = os.path.join(dir_name, file_name)
            self._scale_factor = factor
            self._rgb_array = np.array(cv2.imread(self._path))
            self._color_image = Image.fromarray(_apply_scale(factor, self._rgb_array))
            self._gray_image = self._color_image.convert('L')

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def scale_factor(self):
        return self._scale_factor

    @property
    def rgb_array(self):
        return self._rgb_array

    @property
    def color_image(self):
        return self._color_image

    @property
    def gray_image(self):
        return self._gray_image
