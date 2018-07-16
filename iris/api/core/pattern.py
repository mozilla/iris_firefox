# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os

import cv2
import numpy as np

from location import Location
from util.core_helper import get_module_dir, get_images_path

try:
    import Image
except ImportError:
    from PIL import Image

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


def load_all_patterns():
    result_list = []
    for root, dirs, files in os.walk(get_module_dir()):
        for file_name in files:
            if file_name.endswith('.png'):
                if get_images_path() in root or 'common' in root or 'local_web' in root:
                    pattern_name, pattern_scale = _parse_name(file_name)
                    pattern_path = os.path.join(root, file_name)
                    pattern = {'name': pattern_name, 'path': pattern_path, 'scale': pattern_scale}
                    result_list.append(pattern)
    return result_list


_images = load_all_patterns()


class Pattern(object):
    def __init__(self, image_name):
        name, path, scale = get_pattern_details(image_name)
        self._image_name = name
        self._image_path = path
        self._scale_factor = scale
        self._target_offset = None
        self._rgb_array = np.array(cv2.imread(path))
        self._color_image = Image.fromarray(_apply_scale(scale, self._rgb_array))
        self._gray_image = self._color_image.convert('L')

    def target_offset(self, dx, dy):
        """Add offset to Pattern from top left

        :param int dx: x offset from center
        :param int dy: y offset from center
        :return: a new pattern object
        """

        new_pattern = Pattern(self._image_name)
        new_pattern._target_offset = Location(dx, dy)
        return new_pattern

    def get_filename(self):
        return self._image_name

    def get_file_path(self):
        return self._image_path

    def get_target_offset(self):
        return self._target_offset

    def get_scale_factor(self):
        return self._scale_factor

    def get_rgb_array(self):
        return self._rgb_array

    def get_color_image(self):
        return self._color_image

    def get_gray_image(self):
        return self._gray_image


def get_pattern_details(pattern_name):
    result_list = filter(lambda x: x['name'] == pattern_name, _images)
    if len(result_list) > 0:
        res = result_list[0]
        return res['name'], res['path'], res['scale']


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
