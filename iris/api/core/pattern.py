# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import inspect
import logging
import os

import cv2
import numpy as np

from errors import FindError
from errors import APIHelperError
from iris.api.core.platform import Platform
from location import Location
from util.core_helper import IrisCore
from util.core_helper import get_os_version, get_os
from util.parse_args import parse_args
from settings import Settings

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
    if parse_args().resize:
        convert_hi_res_images()
    result_list = []
    for root, dirs, files in os.walk(IrisCore.get_module_dir()):
        for file_name in files:
            if file_name.endswith('.png'):
                if IrisCore.get_images_path() in root or 'common' in root or 'local_web' in root:
                    pattern_name, pattern_scale = _parse_name(file_name)
                    pattern_path = os.path.join(root, file_name)
                    pattern = {'name': pattern_name, 'path': pattern_path, 'scale': pattern_scale}
                    result_list.append(pattern)
    return result_list


def convert_hi_res_images():
    for root, dirs, files in os.walk(IrisCore.get_module_dir()):
        for file_name in files:
            if file_name.endswith('.png'):
                if 'images' in root or 'local_web' in root:
                    if '@' in file_name:
                        logger.debug('Found hi-resolution image at: %s' % os.path.join(root, file_name))
                        temp = file_name.split('@')
                        name = temp[0]
                        scale = int(temp[1].split('x')[0])
                        new_name = '%s.png' % name
                        img = Image.open(os.path.join(root, file_name))
                        logger.debug('Resizing image from %sx scale' % scale)
                        new_img = img.resize((img.width/scale, img.height/scale), Image.ANTIALIAS)
                        logger.debug('Creating newly converted image file at: %s' % os.path.join(root, new_name))
                        new_img.save(os.path.join(root, new_name))
                        logger.debug('Removing unused image at: %s' % os.path.join(root, file_name))
                        os.remove(os.path.join(root, file_name))


_images = load_all_patterns()


class Pattern(object):
    def __init__(self, image_name, from_path=None):
        if from_path is None:
            path = get_image_path(inspect.stack()[1][1], image_name)
        else:
            path = from_path
        name, scale = _parse_name(os.path.split(path)[1])
        self._image_name = name
        self._image_path = path
        self._scale_factor = scale
        self._similarity = Settings.min_similarity
        self._target_offset = None
        self._rgb_array = np.array(cv2.imread(path)) if path is not None else None
        self._color_image = Image.fromarray(_apply_scale(scale, self._rgb_array)) if scale is not None else None
        self._gray_image = self._color_image.convert('L') if scale is not None else None

    def target_offset(self, dx, dy):
        """Add offset to Pattern from top left

        :param int dx: x offset from center
        :param int dy: y offset from center
        :return: a new pattern object
        """
        new_pattern = Pattern(self._image_name, from_path=self._image_path)
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

    @property
    def similarity(self):
        """Getter for the Pattern similarity property."""
        return self._similarity

    @similarity.setter
    def similarity(self, value):
        """Setter for the Pattern similarity property."""
        self._similarity = value

    def similar(self, value):
        """Set the minimum similarity of the given Pattern object to the specified value."""
        if value > 0.99:
            self._similarity = 0.99
        elif 0 <= value <= 0.99:
            self._similarity = value
        else:
            self._similarity = Settings.min_similarity
        return self

    def exact(self):
        """Set the minimum similarity of the given Pattern object to 0.99, which means exact match is required."""
        self._similarity = 0.99
        return self


def get_pattern_details(pattern_name):
    result_list = filter(lambda x: x['name'] == pattern_name, _images)
    if len(result_list) == 0:
        return pattern_name, None, None
    elif len(result_list) > 0:
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


def get_image_path(caller, image):
    """Enforce proper location for all Pattern creation.

    :param caller: Path of calling Python module
    :param image: string filename of image
    :return: Full path to image on disk
    """

    module = os.path.split(caller)[1]
    module_directory = os.path.split(caller)[0]
    parent_directory = os.path.basename(module_directory)
    file_name = image.split('.')[0]
    names = [image, '%s@2x.png' % file_name, '%s@3x.png' % file_name, '%s@4x.png' % file_name]

    # We will look at all possible paths relative to the calling file, with this priority:
    #
    # - current platform locale folder
    # - common locale folder
    # - current platform root
    # - common root
    #
    # Each directory is scanned for four possible file names, depending on resolution.
    # If the above fails, we will look up the file name in the list of project-wide images,
    # and return whatever we find, with a warning message.
    # If we find nothing, we will raise an exception.
    if Settings.get_os_version() == 'win7':
        os_version = 'win7'
    else:
        os_version = Settings.get_os()
    paths = []
    current_locale = parse_args().locale

    platform_directory = os.path.join(module_directory, 'images', os_version)
    platform_locale_directory = os.path.join(platform_directory, current_locale)
    for name in names:
        paths.append(os.path.join(platform_locale_directory, name))

    common_directory = os.path.join(module_directory, 'images', 'common')
    common_locale_directory = os.path.join(common_directory, current_locale)
    for name in names:
        paths.append(os.path.join(common_locale_directory, name))

    for name in names:
        paths.append(os.path.join(platform_directory, name))

    for name in names:
        paths.append(os.path.join(common_directory, name))

    found = False
    image_path = None
    for path in paths:
        if os.path.exists(path):
            found = True
            image_path = path
            break

    if found:
        logger.debug('Module %s requests image %s' % (module, image))
        logger.debug('Found %s' % image_path)
        return image_path
    else:
        # If not found in correct location, fall back to global image search for now.
        result_list = filter(lambda x: x['name'] == image, _images)
        if len(result_list) > 0:
            res = result_list[0]
            logger.warning('Failed to find image %s in default locations for module %s.' % (image, module))
            logger.warning('Using this one instead: %s' % res['path'])
            logger.warning('Please move image to correct location relative to caller.')
            location_1 = os.path.join(parent_directory, 'images', 'common')
            location_2 = os.path.join(parent_directory, IrisCore.get_images_path())
            logger.warning('Suggested locations: %s, %s' % (location_1, location_2))
            return res['path']
        else:
            logger.error('Pattern creation for %s failed for caller %s.' % (image, caller))
            logger.error('Image not found. Either it is in the wrong platform folder, or it does not exist.')
            logger.debug('Paths searched:')
            logger.debug('\n'.join(paths))
            raise FindError('Pattern not found')
