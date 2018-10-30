# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import cv2
import inspect
import logging
import numpy as np

from errors import FindError
from location import Location
from settings import Settings
from util.core_helper import IrisCore
from util.parse_args import parse_args

try:
    import Image
except ImportError:
    from PIL import Image

logger = logging.getLogger(__name__)


class Pattern(object):
    """A pattern is used to associate an image file with additional attributes used in find operations.

    While using a Region.find() operation, if only an image file is provided, Iris searches the region using a default
    minimum similarity of 0.8. This default value can be changed in Settings.min_similarity. Using similar() you can
    associate a specific similarity value, that will be used as the minimum value, when this pattern object is searched.
    """

    def __init__(self, image_name, from_path=None):

        if from_path is None:
            path = _get_image_path(inspect.stack()[1][1], image_name)
        else:
            path = from_path
        name, scale = _parse_name(os.path.split(path)[1])

        image = cv2.imread(path)

        self.image_name = name
        self.image_path = path
        self.scale_factor = scale
        self.similarity = Settings.min_similarity
        self._target_offset = None
        self._size = _get_pattern_size(image, scale)
        self.rgb_array = _get_rgb_array(image)
        self.color_image = _get_image_from_array(scale, self.rgb_array)
        self.gray_image = _get_gray_image(self.color_image)

    def __str__(self):
        return '(%s, %s, %s, %s)' % (self.image_name, self.image_path, self.scale_factor, self.similarity)

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.image_name, self.image_path,
                                       self.scale_factor, self.similarity)

    def target_offset(self, dx, dy):
        """Add offset to Pattern from top left.

        :param int dx: x offset from center.
        :param int dy: y offset from center.
        :return: A new pattern object.
        """
        new_pattern = Pattern(self.image_name, from_path=self.image_path)
        new_pattern._target_offset = Location(dx, dy)
        return new_pattern

    def get_filename(self):
        """Getter for the image_name property."""
        return self.image_name

    def get_file_path(self):
        """Getter for the image_path property."""
        return self.image_path

    def get_target_offset(self):
        """Getter for the target_offset property."""
        return self._target_offset

    def get_scale_factor(self):
        """Getter for the scale_factor property."""
        return self.scale_factor

    def get_rgb_array(self):
        """Getter for the RGB array of image."""
        return self.rgb_array

    def get_color_image(self):
        """Getter for the color_image property."""
        return self.color_image

    def get_gray_image(self):
        """Getter for the gray_image property."""
        return self.gray_image

    def similar(self, value):
        """Set the minimum similarity of the given Pattern object to the specified value."""
        if value > 0.99:
            self.similarity = 0.99
        elif 0 <= value <= 0.99:
            self.similarity = value
        else:
            self.similarity = Settings.min_similarity
        return self

    def exact(self):
        """Set the minimum similarity of the given Pattern object to 0.99, which means exact match is required."""
        self.similarity = 0.99
        return self

    def get_size(self):
        """Getter for the _size property."""
        return self._size


def _parse_name(full_name):
    """Detects the scale factor in image name.

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


def _load_all_patterns():
    """Function returns a list with all the project's Patterns."""
    if parse_args().resize:
        _convert_hi_res_images()
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


def _convert_hi_res_images():
    """Function resizes all the project's hi-resolution images."""
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
                        new_img = img.resize((img.width / scale, img.height / scale), Image.ANTIALIAS)
                        logger.debug('Creating newly converted image file at: %s' % os.path.join(root, new_name))
                        new_img.save(os.path.join(root, new_name))
                        logger.debug('Removing unused image at: %s' % os.path.join(root, file_name))
                        os.remove(os.path.join(root, file_name))


def _apply_scale(scale, rgb_array):
    """Resize the image for HD images.

    :param scale: Scale of image.
    :param rgb_array: RGB array of image.
    :return: Scaled image.
    """
    if scale > 1:
        temp_h, temp_w, not_needed = rgb_array.shape
        new_w, new_h = int(temp_w / scale), int(temp_h / scale)
        return cv2.resize(rgb_array, (new_w, new_h), interpolation=cv2.INTER_AREA)
    else:
        return rgb_array


def _get_rgb_array(image):
    """Returns np array from an Image."""
    if image is None:
        return None
    return np.array(image)


def _get_pattern_size(image, scale):
    if image is None or scale is None:
        return None
    height, width, channel = image.shape
    return int(width / scale), int(height / scale)


def _get_image_from_array(scale, array):
    """Converts a scaled array into Image."""
    if scale is None or array is None:
        return None
    return Image.fromarray(_apply_scale(scale, array))


def _get_gray_image(colored_image):
    """Converts colored image to gray image."""
    if colored_image is None:
        return None
    return colored_image.convert('L')


def _get_image_path(caller, image):
    """Enforce proper location for all Pattern creation.

    :param caller: Path of calling Python module.
    :param image: String filename of image.
    :return: Full path to image on disk.
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
        result_list = filter(lambda x: x['name'] == image, _load_all_patterns())
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
            raise FindError('Pattern not found.')
