# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os
import platform
import time
from datetime import datetime

import cv2
import numpy as np
import pyautogui
import pyperclip
import pytesseract
import copy

from helpers.image_remove_noise import process_image_for_ocr, OCR_IMAGE_SIZE
from errors import *

try:
    import Image
except ImportError:
    from PIL import Image

pyautogui.FAILSAFE = False
DEFAULT_ACCURACY = 0.7
DEFAULT_TIMEOUT = 3
FIND_METHOD = cv2.TM_CCOEFF_NORMED
DEBUG = True
INVALID_GENERIC_INPUT = 'Invalid input'
INVALID_NUMERIC_INPUT = 'Expected numeric value'
DEFAULT_INTERVAL = 0.5

_images = {}

SUCCESS_LEVEL_NUM = 35
logging.addLevelName(SUCCESS_LEVEL_NUM, 'SUCCESS')


def success(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)


logging.Logger.success = success
logger = logging.getLogger(__name__)


def get_os():
    current_system = platform.system()
    current_os = ''
    if current_system == 'Windows':
        current_os = 'win'
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    elif current_system == 'Linux':
        current_os = 'linux'
        pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
    elif current_system == 'Darwin':
        current_os = 'osx'
        pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
    else:
        logger.error('Iris does not yet support your current environment: ' + current_system)

    return current_os


def get_platform():
    return platform.machine()


def get_module_dir():
    return os.path.realpath(os.path.split(__file__)[0] + '/../..')


CURRENT_PLATFORM = get_os()
PROJECT_BASE_PATH = get_module_dir()

for root, dirs, files in os.walk(PROJECT_BASE_PATH):
    for file_name in files:
        if file_name.endswith('.png'):
            if CURRENT_PLATFORM in root:
                _images[file_name] = os.path.join(root, file_name)

"""
pyautogui.size() works correctly everywhere except Mac Retina
This technique works everywhere, so we'll use it instead
"""

screen_width, screen_height = pyautogui.screenshot().size

image_debug_path = get_module_dir() + '/image_debug'
try:
    os.stat(image_debug_path)
except:
    os.mkdir(image_debug_path)
for debug_image_file in os.listdir(image_debug_path):
    file_path = os.path.join(image_debug_path, debug_image_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        continue


class KeyModifier(object):
    SHIFT = 1 << 0  # 1
    CTRL = 1 << 1  # 2
    CMD = 1 << 2  # 4
    WIN = 1 << 2  # 4
    ALT = 1 << 3  # 8

    @staticmethod
    def get_active_modifiers(value):
        all_modifiers = [
            (KeyModifier.SHIFT, "shift"),
            (KeyModifier.CTRL, "ctrl")]

        if get_os() == "osx":
            all_modifiers.append((KeyModifier.CMD, "command"))
        else:
            # TODO: verify that Linux is same as Windows
            all_modifiers.append((KeyModifier.WIN, "win"))

        all_modifiers.append((KeyModifier.ALT, "alt"))

        active_modifiers = []
        for item in all_modifiers:
            if item[0] & value:
                active_modifiers.append(item[1])
        return active_modifiers


class _key(object):

    def __init__(self, label, reserved=True):
        self.value = label
        self.is_reserved = reserved

    def __str__(self):
        return self.value


class Key(object):
    SPACE = _key(" ")
    TAB = _key("tab")
    ALT = _key("alt")
    ENTER = _key("enter")
    LEFT = _key("left")
    RIGHT = _key("right")
    UP = _key("up")
    DOWN = _key("down")
    ESC = _key("esc")
    HOME = _key("home")
    END = _key("end")
    DELETE = _key("del")
    FN = _key("fn")
    F2 = _key("f2")
    F5 = _key("f5")
    F6 = _key("f6")
    F11 = _key("f11")


class Pattern(object):
    def __init__(self, image_name):
        self.image_name = image_name
        self.image_path = _images[self.image_name]
        self.target_offset = Location(0, 0)

    def targetOffset(self, dx, dy):
        """ Add offset to Pattern from top left

        :param int dx: x offset from center
        :param int dy: y offset from center
        :return: a new pattern object
        """

        new_pattern = Pattern(self.image_name)
        new_pattern.target_offset = Location(dx, dy)
        return new_pattern

    def getFilename(self):
        return self.image_name

    def getFilepath(self):
        return self.image_path

    def getTargetOffset(self):
        """

        :return: Location object as the target offset
        """
        return self.target_offset


class Location(object):
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def getX(self):
        return self._x

    def setX(self, new_x):
        if isinstance(new_x, int):
            self._x = new_x
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    x = property(getX, setX)

    def getY(self):
        return self._y

    def setY(self, new_y):
        if isinstance(new_y, int):
            self._y = new_y
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    y = property(getY, setY)

    def setLocation(self, x=0, y=0):
        self._x = x
        self._y = y

    def offset(self, away_x, away_y):
        new_x = int(self.x + away_x)
        new_y = int(self.y + away_y)
        return Location(new_x, new_y)

    def above(self, away_y):
        new_y = int(self.y - away_y)
        return Location(self.x, new_y)

    def below(self, away_y):
        new_y = int(self.y + away_y)
        return Location(new_y)

    def left(self, away_x):
        new_x = int(self.x - away_x)
        return Location(new_x, self.y)

    def right(self, away_x):
        new_x = int(self.x + away_x)
        return Location(new_x, self.y)


class Region(object):
    def __init__(self, x=0, y=0, w=0, h=0):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def getX(self):
        return self._x

    def setX(self, new_x):
        if isinstance(new_x, int):
            self._x = new_x
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    x = property(getX, setX)

    def getY(self):
        return self._y

    def setY(self, new_y):
        if isinstance(new_y, int):
            self._y = new_y
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    y = property(getY, setY)

    def getW(self):
        return self._w

    def setW(self, new_w):
        if isinstance(new_w, int):
            self._w = new_w
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    w = property(getW, setW)

    def getH(self):
        return self._h

    def setH(self, new_h):
        if isinstance(new_h, int):
            self._h = new_h
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    h = property(getH, setH)

    def getCenter(self):
        center_x = int(self.x + self.w) / 2
        center_y = int(self.y + self.h) / 2
        return Location(center_x, center_y)

    def moveTo(self, new_location):
        self.x = new_location.getX()
        self.y = new_location.getY()

    def getTopLeft(self):
        return Location(self.x, self.y)

    def getTopRight(self):
        top_right_x = self.x + self.w
        return Location(top_right_x, self.y)

    def getBottomLeft(self):
        bottom_left_y = self.y + self.h
        return Location(self.x, bottom_left_y)

    def getBottomRight(self):
        bottom_right_x = self.x + self.w
        bottom_right_y = self.y + self.h
        return Location(bottom_right_x, bottom_right_y)

    def hover(self, where=None, duration=0):
        return hover(where, duration, self)

    def find(self, what=None, precision=DEFAULT_ACCURACY):
        return find(what, precision, self)

    def findAll(self, what=None, precision=DEFAULT_ACCURACY):
        return findAll(what, precision, self)

    def wait(self, what=None, timeout=DEFAULT_TIMEOUT, precision=DEFAULT_ACCURACY):
        return wait(what, timeout, precision, self)

    def exists(self, what=None, timeout=DEFAULT_TIMEOUT, precision=DEFAULT_ACCURACY):
        return exists(what, timeout, precision, self)

    def click(self, where=None, duration=DEFAULT_INTERVAL):
        return click(where, duration, self)

    def text(self, search_for=None):
        return _text_search_all(self)


def _save_debug_image(search_for, on_region, locations):
    """ Saves input Image for debug.

    :param Image search_for: Input needle image that needs to be highlighted
    :param Image on_region: Input Region as Image
    :param List[Location] || Location locations: Location or list of Location as coordinates
    :return: None
    """
    if DEBUG:
        on_region = cv2.cvtColor(on_region, cv2.COLOR_GRAY2BGR)
        w, h = search_for.shape[::-1]

        def _draw_rectangle(on_what, (top_x, top_y), (btm_x, btm_y)):
            cv2.rectangle(on_what, (top_x, top_y), (btm_x, btm_y), (0, 0, 255), 2)

        if isinstance(locations, list):
            for location in locations:
                if isinstance(location, Location):
                    _draw_rectangle(on_region, (location.x, location.y), (location.x + w, location.y + h))

        elif isinstance(locations, Location):
            _draw_rectangle(on_region, (locations.x, locations.y), (locations.x + w, locations.y + h))

        current_time = datetime.now()
        temp_f = str(current_time).replace(' ', '_').replace(':', '_').replace('.', '_').replace('-', '_') + '.jpg'
        cv2.imwrite(image_debug_path + '/' + temp_f, on_region)


def _save_ocr_debug_image(on_region, matches):
    if matches is None:
        return
    if isinstance(matches, list):
        for mt in matches:
            cv2.rectangle(on_region,
                          (mt['x'], mt['y']), (mt['x'] + mt['width'], mt['y'] + mt['height']), (0, 0, 255), 6)

    current_time = datetime.now()
    temp_f = str(current_time).replace(' ', '_').replace(':', '_').replace('.', '_').replace('-', '_') + '.jpg'
    cv2.imwrite(image_debug_path + '/' + temp_f, on_region)


def _region_grabber(coordinates):
    """ Returns a screenshot based on input coordinates

    :param tuple coordinates: top_left_x, top_left_y, width, height
    :return: Image object
    """
    grabbed_area = pyautogui.screenshot(region=coordinates)

    if get_os() is 'osx':
        # Resize grabbed area to what pyautogui thinks is the correct screen size
        # TODO double check this on mac since resizing for regions deforms images
        w, h = pyautogui.size()
        logger.debug('Screen size according to pyautogui.size(): %s,%s' % (w, h))
        logger.debug('Screen size according to pyautogui.screenshot().size: %s,%s' % (screen_width, screen_height))
        resized_area = grabbed_area.resize([w, h])
        return resized_area
    else:
        return grabbed_area


def _match_template(search_for, haystack, precision=DEFAULT_ACCURACY):
    """Search for needle in stack ( single match )

    :param str search_for: Image path ( needle )
    :param Image haystack: Region as Image ( haystack )
    :param float precision: Min allowed similarity
    :return: Location
    """
    img_rgb = np.array(haystack)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    needle = cv2.imread(search_for, 0)

    try:
        res = cv2.matchTemplate(img_gray, needle, FIND_METHOD)
    except:
        return Location(-1, -1)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val < precision:
        return Location(-1, -1)
    else:
        position = Location(max_loc[0], max_loc[1])
        _save_debug_image(needle, img_gray, position)
        return position


def _match_template_multiple(search_for, haystack, precision=DEFAULT_ACCURACY, threshold=0.7):
    """Search for needle in stack ( multiple matches )

    :param str search_for:  Image path ( needle )
    :param Image haystack: Region as Image ( haystack )
    :param float precision: Min allowed similarity
    :param float threshold:  Max threshold
    :return: List of Location
    """
    img_rgb = np.array(haystack)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    needle = cv2.imread(search_for, 0)

    try:
        res = cv2.matchTemplate(img_gray, needle, FIND_METHOD)
    except:
        return Location(-1, -1)

    w, h = needle.shape[::-1]
    points = []
    while True:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if FIND_METHOD in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        if threshold < max_val < precision:
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

    _save_debug_image(needle, img_gray, points)
    return points


def _image_search(image_path, precision=DEFAULT_ACCURACY, region=None):
    """ Wrapper over _match_template. Search image in a Region or full screen

    :param str image_path: Image path ( needle )
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """
    if isinstance(region, Region):
        stack_image = _region_grabber(coordinates=(region.getX(), region.getY(), region.getW(), region.getH()))
    else:
        stack_image = _region_grabber(coordinates=(0, 0, screen_width, screen_height))

    return _match_template(image_path, stack_image, precision)


def _image_search_multiple(image_path, precision=DEFAULT_ACCURACY, region=None):
    """ Wrapper over _match_template_multiple. Search image ( multiple ) in a Region or full screen

    :param str image_path: Image path ( needle )
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: List[Location]
    """
    if isinstance(region, Region):
        stack_image = _region_grabber(coordinates=(region.getX(), region.getY(), region.getW(), region.getH()))
    else:
        stack_image = _region_grabber(coordinates=(0, 0, screen_width, screen_height))
    return _match_template_multiple(image_path, stack_image, precision)


def _image_search_loop(image_path, at_interval=DEFAULT_INTERVAL, attempts=5, precision=DEFAULT_ACCURACY, region=None):
    """ Search for an image ( in loop ) in a Region or full screen

    :param str image_path: Image path ( needle )
    :param float at_interval: Wait time between searches
    :param int attempts: Number of max attempts
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """
    pos = _image_search(image_path, precision, region)
    tries = 0
    while pos.x is -1 and tries < attempts:
        logger.debug("Searching for image %s" % image_path)
        time.sleep(at_interval)
        pos = _image_search(image_path, precision, region)
        tries += 1
    return pos


def _text_search_all(in_region=None):
    if in_region is None:
        stack_image = _region_grabber(coordinates=(0, 0, screen_width, screen_height))

    if isinstance(in_region, Region):
        stack_image = _region_grabber(
            coordinates=(in_region.getX(), in_region.getY(), in_region.getW(), in_region.getH()))

    tesseract_match_min_len = 12
    input_image = np.array(stack_image)
    optimized_ocr_image = process_image_for_ocr(image_array=Image.fromarray(input_image))

    optimized_ocr_array = np.array(optimized_ocr_image)
    processed_data = pytesseract.image_to_data(Image.fromarray(optimized_ocr_array))

    debug_img = cv2.cvtColor(optimized_ocr_array, cv2.COLOR_GRAY2BGR)

    length_x, width_y = stack_image.size
    dpi_factor = max(1, int(OCR_IMAGE_SIZE / length_x))

    final_data = []
    debug_data = []

    for line in processed_data.split('\n'):
        try:
            data = line.encode('ascii').split()
            if len(data) is tesseract_match_min_len:
                precision = int(data[10]) / float(100)
                virtual_data = {'x': int(data[6]),
                                'y': int(data[7]),
                                'width': int(data[8]),
                                'height': int(data[9]),
                                'precision': float(precision),
                                'value': str(data[11])
                                }
                debug_data.append(virtual_data)

                left_offset = 0
                top_offset = 0
                if isinstance(in_region, Region):
                    left_offset = in_region.getX()
                    top_offset = in_region.getY()

                # Scale down coordinates since actual screen has different dpi
                screen_data = copy.deepcopy(virtual_data)
                screen_data['x'] = screen_data['x'] / dpi_factor + left_offset
                screen_data['y'] = screen_data['y'] / dpi_factor + top_offset
                screen_data['width'] = screen_data['width'] / dpi_factor
                screen_data['height'] = screen_data['height'] / dpi_factor

                final_data.append(screen_data)
        except:
            continue

    _save_ocr_debug_image(debug_img, debug_data)
    return final_data


"""Sikuli wrappers

- wait
- waitVanish
- click
- exists 
- find
- findAll
- type
- Key
- KeyModifier
"""


def _get_needle_path(string_or_pattern):
    """ Helper for getting image path

    :param str || Pattern string_or_pattern: Image name or Pattern object
    :return: string of image path
    """
    if isinstance(string_or_pattern, Pattern):
        return string_or_pattern.image_path
    elif isinstance(string_or_pattern, str):
        if string_or_pattern in _images:
            return _images[string_or_pattern]
        else:
            raise ValueError('Unknown image name: %s' % string_or_pattern)
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def hover(where=None, duration=0, in_region=None):
    """Hover over a Location, Pattern or image

    :param where: Location, Pattern or image name for hover target
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """
    if isinstance(where, Location):
        pyautogui.moveTo(where.x, where.y, duration)

    elif isinstance(where, str) or isinstance(where, Pattern):
        image_path = _get_needle_path(where)
        pos = _image_search(image_path, region=in_region)
        if pos.x is not -1:
            if isinstance(where, Pattern):
                possible_offset = where.getTargetOffset()
                move_to = Location(pos.x + possible_offset.getX(), pos.y + possible_offset.getY())
                pyautogui.moveTo(move_to.x, move_to.y)
            else:
                pyautogui.moveTo(pos.x, pos.y)
        else:
            raise FindError('Unable to find image %s' % image_path)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def find(what, precision=DEFAULT_ACCURACY, in_region=None):
    """Look for a single match of a Pattern or image

    :param what: String or Pattern
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: Location
    """
    if isinstance(what, str) or isinstance(what, Pattern):
        image_path = _get_needle_path(what)
        return _image_search(image_path, precision, in_region)
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def findAll(what, precision=DEFAULT_ACCURACY, in_region=None):
    """Look for multiple matches of a Pattern or image

    :param what: String or Pattern
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return:
    """
    if isinstance(what, str) or isinstance(what, Pattern):
        image_path = _get_needle_path(what)
        return _image_search_multiple(image_path, precision, in_region)
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def wait(image, timeout=DEFAULT_TIMEOUT, precision=DEFAULT_ACCURACY, in_region=None):
    """Wait for a Pattern or image to appear

    :param image: String or Pattern
    :param timeout: Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if found
    """
    if isinstance(image, str) or isinstance(image, Pattern):
        s_interval = DEFAULT_INTERVAL
        max_attempts = int(timeout / s_interval)

        image_path = _get_needle_path(image)
        image_found = _image_search_loop(image_path, s_interval, max_attempts, precision, in_region)
        if (image_found.x != -1) & (image_found.y != -1):
            return True
        else:
            raise FindError('Unable to find image %s' % image_path)
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def exists(image, timeout=DEFAULT_TIMEOUT, precision=DEFAULT_ACCURACY, in_region=None):
    """Check if Pattern or image exists

    :param image: String or Pattern
    :param timeout: Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if found
    """
    try:
        wait(image, timeout, precision, in_region)
        return True
    except FindError:
        return False


def waitVanish(image, timeout=DEFAULT_TIMEOUT, precision=DEFAULT_ACCURACY, in_region=None):
    """Wait until a Pattern or image disappears

    :param image: Image, Pattern or string
    :param timeout:  Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if vanished
    """
    interval = DEFAULT_INTERVAL
    max_attempts = int(timeout / interval)
    pattern_found = True
    tries = 0
    while (pattern_found is True) and (tries < max_attempts):
        time.sleep(interval)
        try:
            pattern_found = wait(image, 1, precision, in_region)
        except FindError:
            pattern_found = False
        tries += 1

    if pattern_found is True:
        raise FindError('Unable to find %s' % image)
    else:
        return True


def _click_pattern(pattern, clicks=None, duration=DEFAULT_INTERVAL, in_region=None, button=None):
    """Click on center or offset of a Pattern

    :param pattern: Input Pattern
    :param clicks: Number of mouse clicks
    :param duration: Speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3)
    :return: None
    """
    needle = cv2.imread(pattern.image_path)
    height, width, channels = needle.shape
    p_top = _image_search(pattern.image_path, DEFAULT_ACCURACY, in_region)

    possible_offset = pattern.getTargetOffset()

    if possible_offset.x > 0 or possible_offset.y > 0:
        _click_at(Location(p_top.x + possible_offset.x, p_top.y + possible_offset.y), clicks, duration, button)
    else:
        _click_at(Location(p_top.x + width / 2, p_top.y + height / 2), clicks, duration, button)


def _click_at(location=None, clicks=None, duration=DEFAULT_INTERVAL, button=None):
    """Click on Location coordinates

    :param location: Location , image name or Pattern
    :param clicks: Number of mouse clicks
    :param duration: speed of hovering from current location to target
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3)
    :return: None
    """
    if location is None:
        location = Location(0, 0)
    pyautogui.moveTo(location.x, location.y, duration)
    pyautogui.click(clicks=clicks, interval=0.0, button=button)


def _general_click(where=None, clicks=None, duration=DEFAULT_INTERVAL, in_region=None, button=None):
    """General Mouse Click

    :param where: Location , image name or Pattern
    :param clicks: Number of mouse clicks
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3)
    :return: None
    """
    if isinstance(where, Location):
        _click_at(where, clicks, duration, button)

    elif isinstance(where, str):
        pattern = Pattern(where)
        _click_pattern(pattern, clicks, duration, in_region, button)

    elif isinstance(where, Pattern):
        _click_pattern(where, clicks, duration, in_region, button)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def click(where=None, duration=DEFAULT_INTERVAL, in_region=None):
    """Mouse left click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """
    _general_click(where, 1, duration, in_region, 'left')


def rightClick(where=None, duration=DEFAULT_INTERVAL, in_region=None):
    """Mouse right click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """
    _general_click(where, 1, duration, in_region, 'right')


def doubleClick(where=None, duration=DEFAULT_INTERVAL, in_region=None):
    """Mouse double click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """
    _general_click(where, 2, duration, in_region, 'left')


def _to_location(pattern_or_string=None, in_region=None):
    """Transform pattern or string to location

    :param pattern_or_string: Pattern or string input
    :param in_region: Region object in order to minimize the area
    :return: Location object
    """
    if isinstance(pattern_or_string, Pattern):
        return _image_search(pattern_or_string.image_path, DEFAULT_ACCURACY, in_region)
    elif isinstance(pattern_or_string, str):
        return _image_search(_get_needle_path(pattern_or_string), DEFAULT_ACCURACY, in_region)
    elif isinstance(pattern_or_string, Location):
        return pattern_or_string


def dragDrop(drag_from, drop_to, duration=DEFAULT_INTERVAL):
    """Mouse drag and drop

    :param drag_from: Starting point for drag and drop. Can be pattern, string or location
    :param drop_to: Ending point for drag and drop. Can be pattern, string or location
    :param duration: speed of drag and drop
    :return: None
    """
    from_location = _to_location(drag_from)
    to_location = _to_location(drop_to)
    pyautogui.moveTo(from_location.x, from_location.y, 0)
    pyautogui.dragTo(to_location.x, to_location.x, duration)


def get_screen():
    """Returns full screen Image."""
    return _region_grabber(coordinates=(0, 0, screen_width, screen_height))


def keyDown(key):
    if isinstance(key, _key):
        pyautogui.keyDown(str(key))
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyDown(key)
        else:
            raise ValueError("Unsupported string input")
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def keyUp(key):
    if isinstance(key, _key):
        pyautogui.keyUp(str(key))
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyUp(key)
        else:
            raise ValueError("Unsupported string input")
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def scroll(clicks):
    pyautogui.scroll(clicks)


def paste(text):
    # load to clipboard
    pyperclip.copy(text)
    if get_os() is 'osx':
        pyautogui.hotkey('command', 'v')
    else:
        pyautogui.hotkey('ctrl', 'v')
    # clear clipboard
    pyperclip.copy('')


def type(text=None, modifier=None, interval=0.02):
    logger.debug('type method: ')
    if modifier is None:
        if isinstance(text, _key):
            logger.debug('Scenario 1: reserved key')
            logger.debug('Reserved key: %s' % text)
            if str(text) is str(Key.ENTER):
                pyautogui.typewrite(['enter'])
            else:
                pyautogui.keyDown(str(text))
                pyautogui.keyUp(str(text))
        else:
            logger.debug('Scenario 2: normal key or text block')
            logger.debug('Text: %s' % text)
            pyautogui.typewrite(text, interval)
    else:
        logger.debug('Scenario 3: combination of modifiers and other keys')
        modifier_keys = KeyModifier.get_active_modifiers(modifier)
        num_keys = len(modifier_keys)
        logger.debug('Modifiers (%s): %s ' % (num_keys, ' '.join(modifier_keys)))
        logger.debug('text: %s' % text)
        if num_keys == 1:
            pyautogui.hotkey(modifier_keys[0], str(text))
        elif num_keys == 2:
            pyautogui.hotkey(modifier_keys[0], modifier_keys[1], str(text))
        else:
            logger.error('Returned key modifiers out of range')
