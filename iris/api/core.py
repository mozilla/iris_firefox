# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import Queue
import copy
import ctypes
import inspect
import logging
import multiprocessing
import os
import platform
import re
import subprocess
import time
from datetime import datetime

import cv2
import numpy as np
import pyautogui
import pyperclip
import pytesseract

from errors import *
from helpers.image_remove_noise import process_image_for_ocr, OCR_IMAGE_SIZE
from helpers.parse_args import parse_args
from location import Location
from core_helper import get_os
from platform_iris import Platform
from settings import Settings, DEFAULT_CLICK_DELAY, DEFAULT_KEY_SHORTCUT_DELAY, DEFAULT_TYPE_DELAY

try:
    import Image
except ImportError:
    from PIL import Image

FIND_METHOD = cv2.TM_CCOEFF_NORMED

logger = logging.getLogger(__name__)

args = parse_args()
run_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')

pyautogui.FAILSAFE = False
save_debug_images = args.level == 10

INVALID_GENERIC_INPUT = 'Invalid input'
INVALID_NUMERIC_INPUT = 'Expected numeric value'

MIN_CPU_FOR_MULTIPROCESSING = 4

SUCCESS_LEVEL_NUM = 35
logging.addLevelName(SUCCESS_LEVEL_NUM, 'SUCCESS')


def success(self, message, *args, **kws):
    """Log 'msg % args' with severity 'SUCCESS' (level = 35).

    To pass exception information, use the keyword argument exc_info with
    a true value, e.g.

    logger.success('Houston, we have a %s', 'thorny problem', exc_info=1)
    """
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)


logging.Logger.success = success
logger = logging.getLogger(__name__)


def get_run_id():
    return run_id


def get_platform():
    return platform.machine()


def get_module_dir():
    return os.path.realpath(os.path.split(__file__)[0] + '/../..')


current_platform_pattern = os.path.join('images', get_os())
PROJECT_BASE_PATH = get_module_dir()


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


def load_all_patterns():
    result_list = []
    for root, dirs, files in os.walk(PROJECT_BASE_PATH):
        for file_name in files:
            if file_name.endswith('.png'):
                if current_platform_pattern in root or 'common' in root or 'local_web' in root:
                    pattern_name, pattern_scale = _parse_name(file_name)
                    pattern_path = os.path.join(root, file_name)
                    pattern = {'name': pattern_name, 'path': pattern_path, 'scale': pattern_scale}
                    result_list.append(pattern)
    return result_list


_images = load_all_patterns()

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT = pyautogui.screenshot().size

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


def use_multiprocessing():
    return multiprocessing.cpu_count() >= MIN_CPU_FOR_MULTIPROCESSING


class _IrisKey(object):
    def __init__(self, label, value=None, reserved=True):
        self.label = label
        self.value = value
        self.is_reserved = reserved

    def __str__(self):
        return self.label


class Env(object):
    @staticmethod
    def getClipboard():
        return pyperclip.paste()


class Key(object):
    ADD = _IrisKey('add')
    ALT = _IrisKey('alt', 1 << 3)
    BACKSPACE = _IrisKey('backspace')
    CAPS_LOCK = _IrisKey('capslock')
    CMD = _IrisKey('command', 1 << 2)
    CTRL = _IrisKey('ctrl', 1 << 1)
    DELETE = _IrisKey('del')
    DIVIDE = _IrisKey('divide')
    DOWN = _IrisKey('down')
    ENTER = '\n'
    END = _IrisKey('end')
    ESC = _IrisKey('esc')
    F1 = _IrisKey('f1')
    F2 = _IrisKey('f2')
    F3 = _IrisKey('f3')
    F4 = _IrisKey('f4')
    F5 = _IrisKey('f5')
    F6 = _IrisKey('f6')
    F7 = _IrisKey('f7')
    F8 = _IrisKey('f8')
    F9 = _IrisKey('f9')
    F10 = _IrisKey('f10')
    F11 = _IrisKey('f11')
    F12 = _IrisKey('f12')
    F13 = _IrisKey('f13')
    F14 = _IrisKey('f14')
    F15 = _IrisKey('f15')
    HOME = _IrisKey('home')
    INSERT = _IrisKey('insert')
    LEFT = _IrisKey('left')
    META = _IrisKey('winleft', 1 << 2)
    MINUS = _IrisKey('subtract')
    MULTIPLY = _IrisKey('multiply')
    NUM0 = _IrisKey('num0')
    NUM1 = _IrisKey('num1')
    NUM2 = _IrisKey('num2')
    NUM3 = _IrisKey('num3')
    NUM4 = _IrisKey('num4')
    NUM5 = _IrisKey('num5')
    NUM6 = _IrisKey('num6')
    NUM7 = _IrisKey('num7')
    NUM8 = _IrisKey('num8')
    NUM9 = _IrisKey('num9')
    NUM_LOCK = _IrisKey('numlock')
    PAGE_DOWN = _IrisKey('pagedown')
    PAGE_UP = _IrisKey('pageup')
    PAUSE = _IrisKey('pause')
    PRINT_SCREEN = _IrisKey('printscreen')
    RIGHT = _IrisKey('right')
    SCROLL_LOCK = _IrisKey('scrolllock')
    SEPARATOR = _IrisKey('separator')
    SHIFT = _IrisKey('shift', 1 << 0)
    SPACE = ' '
    TAB = '\t'
    UP = _IrisKey('up')
    WIN = _IrisKey('win', 1 << 2)

    # Additional keys
    ACCEPT = _IrisKey('accept')
    ALT_LEFT = _IrisKey('altleft')
    ALT_RIGHT = _IrisKey('altright')
    APPS = _IrisKey('apps')
    BROWSER_BACK = _IrisKey('browserback')
    BROWSER_FAVORITES = _IrisKey('browserfavorites')
    BROWSER_FORWARD = _IrisKey('browserforward')
    BROWSER_HOME = _IrisKey('browserhome')
    BROWSER_REFRESH = _IrisKey('browserrefresh')
    BROWSER_SEARCH = _IrisKey('browsersearch')
    BROWSER_STOP = _IrisKey('browserstop')
    CLEAR = _IrisKey('clear')
    COMMAND = _IrisKey('command')
    CONVERT = _IrisKey('convert')
    CTRL_LEFT = _IrisKey('ctrlleft')
    CTRL_RIGHT = _IrisKey('ctrlright')
    DECIMAL = _IrisKey('decimal')
    EXECUTE = _IrisKey('execute')
    F16 = _IrisKey('f16')
    F17 = _IrisKey('f17')
    F18 = _IrisKey('f18')
    F19 = _IrisKey('f19')
    F20 = _IrisKey('f20')
    F21 = _IrisKey('f21')
    F22 = _IrisKey('f22')
    F23 = _IrisKey('f23')
    F24 = _IrisKey('f24')
    FINAL = _IrisKey('final')
    FN = _IrisKey('fn')
    HANGUEL = _IrisKey('hanguel')
    HANGUL = _IrisKey('hangul')
    HANJA = _IrisKey('hanja')
    HELP = _IrisKey('help')
    JUNJA = _IrisKey('junja')
    KANA = _IrisKey('kana')
    KANJI = _IrisKey('kanji')
    LAUNCH_APP1 = _IrisKey('launchapp1')
    LAUNCH_APP2 = _IrisKey('launchapp2')
    LAUNCH_MAIL = _IrisKey('launchmail')
    LAUNCH_MEDIA_SELECT = _IrisKey('launchmediaselect')
    MODE_CHANGE = _IrisKey('modechange')
    NEXT_TRACK = _IrisKey('nexttrack')
    NONCONVERT = _IrisKey('nonconvert')
    OPTION = _IrisKey('option')
    OPTION_LEFT = _IrisKey('optionleft')
    OPTION_RIGHT = _IrisKey('optionright')
    PGDN = _IrisKey('pgdn')
    PGUP = _IrisKey('pgup')
    PLAY_PAUSE = _IrisKey('playpause')
    PREV_TRACK = _IrisKey('prevtrack')
    PRINT = _IrisKey('print')
    PRNT_SCRN = _IrisKey('prntscrn')
    PRTSC = _IrisKey('prtsc')
    PRTSCR = _IrisKey('prtscr')
    RETURN = _IrisKey('return')
    SELECT = _IrisKey('select')
    SHIFT_LEFT = _IrisKey('shiftleft')
    SHIFT_RIGHT = _IrisKey('shiftright')
    SLEEP = _IrisKey('sleep')
    STOP = _IrisKey('stop')
    SUBTRACT = _IrisKey('subtract')
    VOLUME_DOWN = _IrisKey('volumedown')
    VOLUME_MUTE = _IrisKey('volumemute')
    VOLUME_UP = _IrisKey('volumeup')
    WIN_LEFT = _IrisKey('winleft')
    WIN_RIGHT = _IrisKey('winright')
    YEN = _IrisKey('yen')

    @staticmethod
    def isLockOn(keyboard_key):
        if Settings.getOS() == Platform.WINDOWS:
            hllDll = ctypes.WinDLL("User32.dll")
            if keyboard_key == Key.CAPS_LOCK:
                keyboard_code = 0x14
            elif keyboard_key == Key.NUM_LOCK:
                keyboard_code = 0x90
            elif keyboard_key == Key.SCROLL_LOCK:
                keyboard_code = 0x91
            try:
                keystate = hllDll.GetKeyState(keyboard_code)
            except:
                raise Exception('Unable to run Command')
            if (keystate == 1):
                return True
            else:
                return False
        elif Settings.getOS() == Platform.LINUX or Settings.getOS() == Platform.MAC:
            try:
                cmd = subprocess.Popen('xset q', shell=True, stdout=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                logger.error('Command  failed: %s' % repr(e.cmd))
                raise Exception('Unable to run Command')
            else:
                processed_lock_key = keyboard_key.label
                if 'caps' in processed_lock_key:
                    processed_lock_key = 'Caps'
                elif 'num' in processed_lock_key:
                    processed_lock_key = 'Num'
                elif 'scroll' in processed_lock_key:
                    processed_lock_key = 'Scroll'

                for line in cmd.stdout:
                    if processed_lock_key in line:
                        value = ' '.join(line.split())
                        if processed_lock_key in value[0:len(value) / 3]:
                            button = value[0:len(value) / 3]
                            if "off" in button:
                                return False
                            else:
                                return True

                        elif processed_lock_key in value[len(value) / 3:len(value) / 3 + len(value) / 3]:
                            button = value[len(value) / 3:len(value) / 3 + len(value) / 3]
                            if "off" in button:
                                return False
                            else:
                                return True

                        else:
                            button = value[len(value) / 3 * 2:len(value)]
                            if "off" in button:
                                return False
                            else:
                                return True
            finally:
                if Settings.getOS() == Platform.MAC:
                    shutdown_process('Xquartz')


class KeyModifier(object):
    SHIFT = Key.SHIFT.value
    CTRL = Key.CTRL.value
    CMD = Key.CMD.value
    WIN = Key.WIN.value
    META = Key.META.value
    ALT = Key.ALT.value

    @staticmethod
    def get_active_modifiers(value):
        all_modifiers = [
            Key.SHIFT,
            Key.CTRL]
        if Settings.getOS() == Platform.MAC:
            all_modifiers.append(Key.CMD)
        elif Settings.getOS() == Platform.WINDOWS:
            all_modifiers.append(Key.WIN)
        else:
            all_modifiers.append(Key.META)

        all_modifiers.append(Key.ALT)

        active_modifiers = []
        for item in all_modifiers:
            if item.value & value:
                active_modifiers.append(item.label)
        return active_modifiers


# todo Refactor this
class Screen(object):
    def __init__(self, screen_id=0):
        self.id = screen_id

    def capture(self, *args):
        f_arg = args[0]

        if f_arg is None:
            return

        elif isinstance(f_arg, Region):
            return _region_grabber(f_arg)

        elif len(args) is 4:
            return _region_grabber((args[0], args[1], args[2], args[3]))

    def getNumberScreens(self):
        return 1

    def getBounds(self):
        dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)
        return dimensions


def get_pattern_details(pattern_name):
    result_list = filter(lambda x: x['name'] == pattern_name, _images)
    if len(result_list) > 0:
        res = result_list[0]
        return res['name'], res['path'], res['scale']


def iris_image_match_template(needle, haystack, precision, threshold=None):
    """Finds a match or a list of matches

    :param needle:  Image details (needle)
    :param haystack: Region as Image (haystack)
    :param float precision: Min allowed similarity
    :param float || None threshold:  Max threshold
    :return: A location or a list of locations
    """
    is_multiple = threshold is not None

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


class Pattern(object):
    def __init__(self, image_name):
        name, path, scale = get_pattern_details(image_name)
        self.image_name = name
        self.image_path = path
        self.scale_factor = scale
        self.target_offset = None
        self.rgb_array = np.array(cv2.imread(path))
        self.color_image = Image.fromarray(_apply_scale(scale, self.rgb_array))
        self.gray_image = self.color_image.convert('L')

    def targetOffset(self, dx, dy):
        """Add offset to Pattern from top left

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

    def scale_factor(self):
        return self.scale_factor

    def rgb_array(self):
        return self.rgb_array

    def color_image(self):
        return self.color_image

    def gray_image(self):
        return self.gray_image


class Region(object):
    def __init__(self, x=0, y=0, w=0, h=0):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def debug(self):
        _save_debug_image(None, self, None)

    def debug_ocr(self, with_image_processing=True):
        return self.text(with_image_processing, True)

    def show(self):
        region_screen = _region_grabber(self)
        region_screen.show()

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

    def find(self, what=None, precision=None):
        return find(what, precision, self)

    def findAll(self, what=None, precision=None):
        return findAll(what, precision, self)

    def wait(self, what=None, timeout=None, precision=None):
        wait(what, timeout, precision, self)

    def waitVanish(self, what=None, timeout=None, precision=None):
        return waitVanish(what, timeout, precision, self)

    def exists(self, what=None, timeout=None, precision=None):
        return exists(what, timeout, precision, self)

    def click(self, where=None, duration=None):
        return click(where, duration, self)

    def text(self, with_image_processing=True, with_debug=False):
        return text(with_image_processing, self, with_debug)

    def type(self, text, modifier, interval):
        return type(text, modifier, interval)

    def dragDrop(self, drag_from, drop_to, duration=None):
        return dragDrop(drag_from, drop_to, duration)

    def doubleClick(self, where, duration):
        return doubleClick(where, duration, self)

    def rightClick(self, where, duration):
        return rightClick(where, duration, self)


def _debug_put_text(on_what, input_text='Text', start=(0, 0)):
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    scale = 1
    thickness = 1

    text_size = cv2.getTextSize(input_text, font, scale * 2, thickness)
    start_point = start or (0, 0)
    cv2.rectangle(on_what,
                  start_point,
                  (start_point[0] + text_size[0][0], start_point[1] + text_size[0][1]),
                  (0, 0, 0),
                  cv2.FILLED)

    cv2.putText(on_what,
                input_text,
                (start_point[0], start_point[1] + text_size[0][1] - text_size[0][1] / 4),
                font,
                scale,
                (255, 255, 255),
                thickness, 64)


def get_test_name():
    white_list = ['general.py']
    all_stack = inspect.stack()
    for stack in all_stack:
        filename = os.path.basename(stack[1])
        method_name = stack[3]
        if filename is not '' and 'tests' in os.path.dirname(stack[1]):
            return filename
        elif filename in white_list:
            return method_name
    return


def _save_debug_image(needle, haystack, locations, not_found=False):
    """Saves input Image for debug.

    :param Image || None needle: Input needle image that needs to be highlighted
    :param Image || Region haystack: Input Region as Image
    :param List[Location] || Location || None locations: Location or list of Location as coordinates
    :return: None
    """
    test_name = get_test_name()

    if test_name is not None:
        is_image = False if isinstance(needle, str) and _is_ocr_text(needle) else True
        w, h = 0, 0

        if isinstance(haystack, Region):
            full_screen = _region_grabber(haystack)
            haystack = np.array(Image.fromarray(np.array(full_screen)).convert('L'))
        else:
            if haystack is not None:
                haystack = np.array(Image.fromarray(np.array(haystack)).convert('RGB'))
            else:
                haystack = _region_grabber(None)

        if needle is None:
            h, w = haystack.shape
        elif is_image:
            w, h = np.array(needle).shape[::-1]

        temp_f = re.sub('[ :.-]', '_', str(datetime.now())) + '_' + test_name.replace('.py', '')

        def _draw_rectangle(on_what, (top_x, top_y), (btm_x, btm_y), width=2):
            cv2.rectangle(on_what, (top_x, top_y), (btm_x, btm_y), (0, 0, 255), width)

        if locations is None:
            if not_found:
                locations = Location(0, 0)
            else:
                temp_f = temp_f + '_debug'
                region_ = Image.fromarray(haystack).size
                try:
                    haystack = cv2.cvtColor(haystack, cv2.COLOR_GRAY2RGB)
                except:
                    pass
                if is_image:
                    _draw_rectangle(haystack, (0, 0), (region_[0], region_[1]), 5)

        if not_found:
            temp_f = temp_f + '_not_found'

            on_region_image = Image.fromarray(haystack)
            if is_image:
                search_for_image = Image.fromarray(np.array(needle))

            tuple_paste_location = (0, on_region_image.size[1] / 4)

            d_image = Image.new("RGB", (on_region_image.size[0], on_region_image.size[1]))
            d_image.paste(on_region_image)
            if is_image:
                d_image.paste(search_for_image, tuple_paste_location)

            d_array = np.array(d_image)

            locations = Location(0, tuple_paste_location[1])

            if is_image:
                _debug_put_text(d_array, '<<< Pattern not found',
                                (search_for_image.size[0] + 10, tuple_paste_location[1]))
            else:
                _debug_put_text(d_array, '<<< Text not found: ' + needle, tuple_paste_location)
            haystack = d_array

        if isinstance(locations, list):
            for location in locations:
                if isinstance(location, Location):
                    _draw_rectangle(haystack, (location.x, location.y), (location.x + w, location.y + h))

        elif isinstance(locations, Location):
            _draw_rectangle(haystack, (locations.x, locations.y), (locations.x + w, locations.y + h))

        cv2.imwrite(image_debug_path + '/' + temp_f + '.jpg', haystack)


def _save_ocr_debug_image(on_region, matches):
    if save_debug_images:
        if matches is None:
            return

        border_line = 2
        if isinstance(matches, list):
            for mt in matches:
                cv2.rectangle(on_region,
                              (mt['x'], mt['y']), (mt['x'] + mt['width'], mt['y'] + mt['height']),
                              (0, 0, 255),
                              border_line)
        current_time = datetime.now()
        temp_f = str(current_time).replace(' ', '_').replace(':', '_').replace('.', '_').replace('-', '_') + '.jpg'
        cv2.imwrite(image_debug_path + '/' + temp_f, on_region)


def get_uhd_details():
    uhd_factor = SCREENSHOT_WIDTH / SCREEN_WIDTH
    is_uhd = True if uhd_factor > 1 else False
    return is_uhd, uhd_factor


def _region_grabber(region=None, for_ocr=False):
    """Grabs image from region or full screen.

    :param Region || None region: Region param
    :return: Image
    """
    is_uhd, uhd_factor = get_uhd_details()

    if isinstance(region, Region):
        r_x = uhd_factor * region.getX() if is_uhd else region.getX()
        r_y = uhd_factor * region.getY() if is_uhd else region.getY()
        w_y = uhd_factor * region.getW() if is_uhd else region.getW()
        h_y = uhd_factor * region.getH() if is_uhd else region.getH()
        grabbed_area = pyautogui.screenshot(region=(r_x, r_y, w_y, h_y))

        if is_uhd and not for_ocr:
            grabbed_area = grabbed_area.resize([region.getW(), region.getH()])
        return grabbed_area

    else:
        grabbed_area = pyautogui.screenshot(region=(0, 0, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT))

        if is_uhd and not for_ocr:
            return grabbed_area.resize([SCREEN_WIDTH, SCREEN_HEIGHT])
        else:
            return grabbed_area


def _match_template(needle, haystack, precision=None):
    """Search for needle in stack (single match).

    :param Pattern needle: Image details (needle)
    :param Image.Image haystack: Region as Image (haystack)
    :param float precision: Min allowed similarity
    :return: Location
    """

    if precision is None:
        precision = Settings.MinSimilarity

    haystack_img_gray = haystack.convert('L')
    needle_img_gray = needle.gray_image

    position = iris_image_match_template(needle_img_gray, haystack_img_gray, precision, None)

    if save_debug_images:
        if position.getX() == -1:
            _save_debug_image(needle_img_gray, np.array(haystack_img_gray), None, True)
        else:
            _save_debug_image(needle_img_gray, haystack_img_gray, position)

    return position


def _match_template_multiple(needle, haystack, precision=None, threshold=0.99):
    """Search for needle in stack (multiple matches)

    :param Pattern needle:  Image details (needle)
    :param Image.Image haystack: Region as Image (haystack)
    :param float precision: Min allowed similarity
    :param float threshold:  Max threshold
    :return: List of Location
    """

    if precision is None:
        precision = Settings.MinSimilarity

    if precision is None:
        precision = Settings.MinSimilarity

    haystack_img_gray = haystack.convert('L')
    needle_img_gray = needle.gray_image

    found_list = iris_image_match_template(needle_img_gray, haystack_img_gray, precision, threshold)

    if save_debug_images:
        _save_debug_image(needle, haystack, found_list)

    return found_list


def _add_positive_image_search_result_in_queue(queue, pattern, precision=None, region=None):
    """Puts result in a queue if image is found

    :param Queue.Queue queue: Queue where the result of the search is added
    :param Pattern pattern: name of the searched image
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return:
    """

    if precision is None:
        precision = Settings.MinSimilarity

    result = _image_search(pattern, precision, region)
    if result.getX() != -1:
        queue.put(result)


def _add_negative_image_search_result_in_queue(queue, pattern, precision=None, region=None):
    """Puts result in a queue if image is NOT found

    :param Queue.Queue queue: Queue where the result of the search is added
    :param Pattern pattern: name of the searched image
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return:
    """

    if precision is None:
        precision = Settings.MinSimilarity

    result = _image_search(pattern, precision, region)
    if result.getX() == -1:
        queue.put(result)


def _image_search(pattern, precision=None, region=None):
    """ Wrapper over _match_template. Search image in a Region or full screen

    :param Pattern pattern: Image details (needle)
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """

    if precision is None:
        precision = Settings.MinSimilarity

    stack_image = _region_grabber(region=region)
    location = _match_template(pattern, stack_image, precision)

    if location.x == -1 or location.y == -1:
        return location
    elif region is not None:
        return Location(location.x + region.x, location.y + region.y)
    else:
        return location


def _image_search_multiple(pattern, precision=None, region=None):
    """ Wrapper over _match_template_multiple. Search image (multiple) in a Region or full screen

    :param Pattern pattern: Image details (needle)
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: List[Location]
    """

    if precision is None:
        precision = Settings.MinSimilarity

    stack_image = _region_grabber(region=region)
    return _match_template_multiple(pattern, stack_image, precision)


def _calculate_interval_max_attempts(timeout=None):
    if timeout is None:
        timeout = Settings.AutoWaitTimeout

    wait_scan_rate = float(Settings.WaitScanRate)
    interval = 1 / wait_scan_rate
    max_attempts = int(timeout * wait_scan_rate)
    return interval, max_attempts


def _positive_image_search_loop(pattern, timeout=None, precision=None, region=None):
    """ Search for an image (in loop) in a Region or full screen

    :param Pattern pattern: name of the searched image
    :param timeout: Number as maximum waiting time in seconds.
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    if precision is None:
        precision = Settings.MinSimilarity

    pos = _image_search(pattern, precision, region)
    tries = 0
    while pos.getX() == -1 and tries < max_attempts:
        logger.debug("Searching for image %s" % pattern)
        time.sleep(interval)
        pos = _image_search(pattern, precision, region)
        tries += 1

    return None if pos.getX() == -1 else pos


def _positive_image_search_multiprocess(pattern, timeout=None, precision=None, region=None):
    """Checks if image is found using multiprocessing

    :param Pattern pattern: name of the searched image
    :param timeout: Number as maximum waiting time in seconds.
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Found image from queue
    """

    out_q = multiprocessing.Queue()

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    if precision is None:
        precision = Settings.MinSimilarity

    process_list = []
    for i in range(max_attempts):
        p = multiprocessing.Process(target=_add_positive_image_search_result_in_queue,
                                    args=(out_q, pattern, precision, region))
        process_list.append(p)
        p.start()
        try:
            return out_q.get(False)
        except Queue.Empty:
            pass
        time.sleep(interval)
        p.join()

        try:
            for process in process_list:
                process.terminate()
        except Exception:
            pass
    return None


def _positive_image_search(pattern, timeout=None, precision=None, region=None):
    if use_multiprocessing():
        return _positive_image_search_multiprocess(pattern, timeout, precision, region)
    else:
        return _positive_image_search_loop(pattern, timeout, precision, region)


def _negative_image_search_loop(pattern, timeout=None, precision=None, region=None):
    """ Search if an image (in loop) is NOT in a Region or full screen

    :param Pattern pattern: name of the searched image
    :param timeout: Number as maximum waiting time in seconds.
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    if precision is None:
        precision = Settings.MinSimilarity

    pattern_found = True
    tries = 0

    while pattern_found is True and tries < max_attempts:
        image_found = _image_search(pattern, precision, region)
        if (image_found.x != -1) & (image_found.y != -1):
            pattern_found = True
        else:
            pattern_found = False
        tries += 1
        time.sleep(interval)

    return None if pattern_found else True


def _negative_image_search_multiprocess(pattern, timeout=None, precision=None, region=None):
    """Checks if image is NOT found or it vanished using multiprocessing

    :param Pattern pattern: name of the searched image
    :param timeout: Number as maximum waiting time in seconds.
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Found image from queue
    """
    out_q = multiprocessing.Queue()

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    if precision is None:
        precision = Settings.MinSimilarity

    process_list = []
    for i in range(max_attempts):
        p = multiprocessing.Process(target=_add_negative_image_search_result_in_queue,
                                    args=(out_q, pattern, precision, region))
        process_list.append(p)
        p.start()
        try:
            return out_q.get(False)
        except Queue.Empty:
            pass
        time.sleep(interval)
        p.join()

        try:
            for process in process_list:
                process.terminate()
        except Exception:
            pass
    return None


def _negative_image_search(pattern, timeout=None, precision=None, region=None):
    if use_multiprocessing():
        return _negative_image_search_multiprocess(pattern, timeout, precision, region)
    else:
        return _negative_image_search_loop(pattern, timeout, precision, region)


def _text_search_all(with_image_processing=True, in_region=None, in_image=None):
    if in_image is None:
        stack_image = _region_grabber(in_region, True)
    else:
        stack_image = in_image

    match_min_len = 12
    input_image = stack_image
    input_image_array = np.array(input_image)
    debug_img = input_image_array

    if with_image_processing:
        input_image = process_image_for_ocr(image_array=input_image)
        input_image_array = np.array(input_image)
        debug_img = cv2.cvtColor(input_image_array, cv2.COLOR_GRAY2BGR)

    processed_data = pytesseract.image_to_data(input_image)

    length_x, width_y = stack_image.size
    dpi_factor = max(1, int(OCR_IMAGE_SIZE / length_x))

    final_data, debug_data = [], []
    is_uhd, uhd_factor = get_uhd_details()

    for line in processed_data.split('\n'):
        try:
            data = line.encode('ascii').split()
            if len(data) is match_min_len:
                precision = int(data[10]) / float(100)
                virtual_data = {'x': int(data[6]),
                                'y': int(data[7]),
                                'width': int(data[8]),
                                'height': int(data[9]),
                                'precision': float(precision),
                                'value': str(data[11])
                                }
                debug_data.append(virtual_data)

                left_offset, top_offset = 0, 0
                scale_divider = uhd_factor if is_uhd else 1

                if isinstance(in_region, Region):
                    left_offset = in_region.getX()
                    top_offset = in_region.getY()

                # Scale down coordinates since actual screen has different dpi
                if with_image_processing:
                    screen_data = copy.deepcopy(virtual_data)
                    screen_data['x'] = screen_data['x'] / dpi_factor / scale_divider + left_offset
                    screen_data['y'] = screen_data['y'] / dpi_factor / scale_divider + top_offset
                    screen_data['width'] = screen_data['width'] / dpi_factor / scale_divider
                    screen_data['height'] = screen_data['height'] / dpi_factor / scale_divider
                    final_data.append(screen_data)
                else:
                    if scale_divider > 1:
                        screen_data = copy.deepcopy(virtual_data)
                        screen_data['x'] = screen_data['x'] / scale_divider
                        screen_data['y'] = screen_data['y'] / scale_divider
                        screen_data['width'] = screen_data['width'] / scale_divider
                        screen_data['height'] = screen_data['height'] / scale_divider
                        final_data.append(screen_data)
        except:
            continue

    # _save_ocr_debug_image(debug_img, debug_data)
    return final_data, debug_img, debug_data


def _combine_text_matches(matches, value):
    new_match = {'x': 0, 'y': 0, 'width': 0, 'height': 0, 'precision': 0.0, 'value': value}

    total_elem = len(matches)

    if total_elem > 0:
        new_match['x'] = matches[0]['x']
        new_match['y'] = matches[0]['y']
        for match in matches:
            new_match['width'] = new_match['width'] + match['width']
            new_match['height'] = new_match['height'] + match['height']
            new_match['precision'] = new_match['precision'] + match['precision']

        new_match['height'] = int(new_match['height'] / total_elem * 1.5)
        new_match['precision'] = new_match['precision'] / total_elem
        return new_match
    else:
        return None


def _text_search_by(what, match_case=True, in_region=None, multiple_matches=False):
    def _search_for_word(local_what, local_text_dict, local_multiple_matches):
        return_multiple = []
        return_single = None

        for local_match_index, local_match_object in enumerate(local_text_dict):
            if local_what == local_match_object['value']:
                if local_multiple_matches:
                    return_multiple.append(local_match_object)
                else:
                    _save_ocr_debug_image(debug_img, [debug_data[local_match_index]])
                    return_single = local_match_object

        return return_multiple, return_single

    def _search_for_phrase(local_what, local_text_dict, local_multiple_matches):
        return_single = None

        matches_string = _ocr_matches_to_string(local_text_dict)
        if local_what not in matches_string:
            return None

        l_what_words = local_what.split()
        l_words_len = len(l_what_words)
        temp_matches = []
        temp_debug = []

        phrase_start_index = matches_string.find(local_what)
        phrase_first_match_index = len(matches_string[0:phrase_start_index].split())

        if l_words_len > 0:
            for local_match_index, local_match_object in enumerate(local_text_dict):
                if local_match_index >= phrase_first_match_index:
                    for word_index, searched_word in enumerate(l_what_words):
                        if searched_word == local_match_object['value']:
                            temp_matches.append(local_match_object)
                            temp_debug.append(debug_data[local_match_index])
            return_single = _combine_text_matches(temp_matches, local_what)
            _save_ocr_debug_image(debug_img, temp_debug)
        return return_single

    if not isinstance(what, str):
        return ValueError(INVALID_GENERIC_INPUT)

    text_dict, debug_img, debug_data = _text_search_all(True, in_region)

    if len(text_dict) <= 0:
        return None

    if not match_case:
        what = what.lower()

    final_m_matches = []
    final_s_match = None

    words_n = len(what.split())
    should_search_phrase = True if words_n > 1 else False

    logger.debug('> All words on region/screen: ' + _ocr_matches_to_string(text_dict))

    if should_search_phrase:
        logger.debug('> Search for phrase: %s' % what)
        final_s_match = _search_for_phrase(what, text_dict, multiple_matches)
    else:
        logger.debug('> Search for word: %s' % what)
        final_m_matches, final_s_match = _search_for_word(what, text_dict, multiple_matches)

    if multiple_matches:
        if len(final_m_matches) > 0:
            return final_m_matches
    else:
        if final_s_match is not None:
            return final_s_match

    # At this point no match was found.
    # Retry matching with auto zoom search over each word

    logger.debug('> No match, try zoom search')

    for match_index, match_object in enumerate(text_dict):
        # Word region
        temp_reg = Region(match_object['x'] - 3, match_object['y'] - 2, match_object['width'] + 6,
                          match_object['height'] + 4)
        zoomed_word_image = _region_grabber(temp_reg)
        w_img_w, w_img_h = zoomed_word_image.size
        # New white image background for zoom in search
        word_background = Image.new('RGBA', (match_object['width'] * 10, match_object['height'] * 5),
                                    (255, 255, 255, 255))

        b_img_w, b_img_h = word_background.size
        # Offset to paste image on center
        offset = ((b_img_w - w_img_w) // 2, (b_img_h - w_img_h) // 2)

        word_background.paste(zoomed_word_image, offset)

        found, debug_img_a, debug_data_a = _text_search_all(True, None, word_background)
        if len(found) > 0:
            text_dict[match_index]['value'] = found[0]['value']
            # _save_ocr_debug_image(debug_img_a, debug_data_a)
            logger.debug('> (Zoom search) new match: %s' % found[0]['value'])
            if what == found[0]['value']:
                break
            if what in _ocr_matches_to_string(text_dict):
                break

    logger.debug('> (Zoom search) All words on region/screen: ' + _ocr_matches_to_string(text_dict))

    if should_search_phrase:
        logger.debug('> Search with zoom for phrase: %s' % what)
        final_s_match = _search_for_phrase(what, text_dict, multiple_matches)
    else:
        logger.debug('> Search with zoom for word: %s' % what)
        final_m_matches, final_s_match = _search_for_word(what, text_dict, multiple_matches)

    if multiple_matches:
        if len(final_m_matches) > 0:
            return final_m_matches
        else:
            if save_debug_images:
                _save_debug_image(what, in_region, None, True)
            return None
    else:
        if final_s_match is not None:
            return final_s_match
        else:
            if save_debug_images:
                _save_debug_image(what, in_region, None, True)
            return None


def _ocr_matches_to_string(matches):
    ocr_string = ''
    for match in matches:
        if match is not None and match['value']:
            ocr_string += ' ' + str(match['value'])
    return ocr_string


def _is_ocr_text(input_text):
    is_ocr_string = True
    pattern_extensions = ('.png', '.jpg')
    if input_text.endswith(pattern_extensions):
        is_ocr_string = False
    return is_ocr_string


def generate_region_by_markers(top_left_marker_img=None, bottom_right_marker_img=None):
    try:
        wait(top_left_marker_img, 10)
        exists(bottom_right_marker_img, 10)
    except Exception as err:
        logger.error('Unable to find page markers')
        raise err

    top_left_pos = find(top_left_marker_img)
    hover(top_left_pos, 0)
    bottom_right_pos = find(bottom_right_marker_img)
    hover(bottom_right_pos, 0)

    marker_width, marker_height = get_asset_img_size(bottom_right_marker_img)

    return Region(top_left_pos.x,
                  top_left_pos.y,
                  (bottom_right_pos.x + marker_width),
                  bottom_right_pos.y - top_left_pos.y + marker_height)


def create_region_from_patterns(top=None, bottom=None, left=None, right=None, padding_top=None, padding_bottom=None,
                                padding_left=None, padding_right=None):
    """
    Returns a region created from combined area of one or more patterns.
    Argument names are just for convenience and don't influence outcome.
    """
    patterns = []
    if top:
        patterns.append(top)
    if bottom:
        patterns.append(bottom)
    if left:
        patterns.append(left)
    if right:
        patterns.append(right)

    if len(patterns) == 0:
        raise ValueError('One or more patterns required.')

    logger.debug('Creating region from %s pattern(s).' % len(patterns))

    a, b = pyautogui.size()
    p1 = Location(a, b)
    p2 = Location(0, 0)

    for pattern in patterns:
        if exists(pattern, 5):
            current_pattern = find(pattern)
            if current_pattern.x < p1.x:
                p1.x = current_pattern.x
            if current_pattern.y < p1.y:
                p1.y = current_pattern.y

            w, h = get_asset_img_size(pattern)

            if current_pattern.x + w > p2.x:
                p2.x = current_pattern.x + w
            if current_pattern.y + h > p2.y:
                p2.y = current_pattern.y + h
        else:
            raise FindError('Pattern not found: %s ' % pattern)

    found_region = Region(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y)

    if padding_top or padding_bottom or padding_left or padding_right:
        logger.debug('Adding padding to region.')

    if padding_top:
        found_region.y -= padding_top
        found_region.h += padding_top

    if padding_bottom:
        found_region.h += padding_bottom

    if padding_left:
        found_region.x -= padding_left
        found_region.w += padding_left

    if padding_right:
        found_region.w += padding_right

    return found_region


class LocalWeb(object):
    """
    Constants that represent URLs and images for local content.
    """

    # Simple blank HTML page
    BLANK_PAGE = 'http://127.0.0.1:%s/blank.htm' % args.port

    # Local Firefox site
    FIREFOX_TEST_SITE = 'http://127.0.0.1:%s/firefox/' % args.port
    FIREFOX_LOGO = 'firefox_logo.png'
    FIREFOX_IMAGE = 'firefox_full.png'
    FIREFOX_BOOKMARK = 'firefox_bookmark.png'
    FIREFOX_BOOKMARK_SMALL = 'firefox_bookmark_small.png'

    # Local Firefox Focus site
    FOCUS_TEST_SITE = 'http://127.0.0.1:%s/focus/' % args.port
    FOCUS_LOGO = 'focus_logo.png'
    FOCUS_IMAGE = 'focus_full.png'
    FOCUS_BOOKMARK = 'focus_bookmark.png'
    FOCUS_BOOKMARK_SMALL = 'focus_bookmark_small.png'

    # Local Mozilla site
    MOZILLA_TEST_SITE = 'http://127.0.0.1:%s/mozilla/' % args.port
    MOZILLA_LOGO = 'mozilla_logo.png'
    MOZILLA_IMAGE = 'mozilla_full.png'
    MOZILLA_BOOKMARK = 'mozilla_bookmark.png'
    MOZILLA_BOOKMARK_SMALL = 'mozilla_bookmark_small.png'

    # Local Pocket site
    POCKET_TEST_SITE = 'http://127.0.0.1:%s/pocket/' % args.port
    POCKET_LOGO = 'pocket_logo.png'
    POCKET_IMAGE = 'pocket_full.png'
    POCKET_BOOKMARK = 'pocket_bookmark.png'
    POCKET_BOOKMARK_SMALL = 'pocket_bookmark_small.png'


def text(with_image_processing=True, in_region=None, debug=False):
    """Get all text from a Region or full screen

    :param bool with_image_processing: With extra dpi and contrast image processing
    :param Region in_region: In certain Region or full screen
    :return: list of matches
    """
    all_text, debug_img, debug_data = _text_search_all(with_image_processing, in_region)
    if debug and debug_img is not None:
        _save_ocr_debug_image(debug_img, debug_data)
        logger.debug('> Found message: %s' % _ocr_matches_to_string(all_text))
    return _ocr_matches_to_string(all_text)


def hover(where=None, duration=0, in_region=None):
    """Hover over a Location, Pattern or image

    :param where: Location, Pattern or image name for hover target
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """
    if isinstance(where, str) and _is_ocr_text(where):
        a_match = _text_search_by(where, True, in_region)
        if a_match is not None:
            pyautogui.moveTo(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        else:
            raise FindError('Unable to find text %s' % where)

    elif isinstance(where, Location):
        pyautogui.moveTo(where.x, where.y, duration)

    elif isinstance(where, str) or isinstance(where, Pattern):

        try:
            pattern = Pattern(where)
        except Exception:
            pattern = where

        pos = _image_search(pattern, region=in_region)
        if pos.x is not -1:
            needle_width, needle_height = get_asset_img_size(pattern.getFilename())
            if isinstance(where, Pattern):
                possible_offset = where.getTargetOffset()
                if possible_offset is not None:
                    move_to = Location(pos.x + possible_offset.getX(), pos.getY() + possible_offset.getY())
                    pyautogui.moveTo(move_to.getX(), move_to.y)
                else:
                    move_to = Location(pos.x, pos.y)
                    pyautogui.moveTo(move_to.getX() + needle_width / 2, move_to.getY() + needle_height / 2)
            else:
                pyautogui.moveTo(pos.x + needle_width / 2, pos.y + needle_height / 2)
        else:
            raise FindError('Unable to find image %s' % pattern.getFilename())

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def find(image_name, precision=None, in_region=None):
    """Look for a single match of a Pattern or image

    :param image_name: String or Pattern
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: Location
    """

    if isinstance(image_name, str) and _is_ocr_text(image_name):
        a_match = _text_search_by(image_name, True, in_region)
        if a_match is not None:
            return Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        else:
            raise FindError('Unable to find text %s' % image_name)

    elif isinstance(image_name, str) or isinstance(image_name, Pattern):

        if precision is None:
            precision = Settings.MinSimilarity

        try:
            pattern = Pattern(image_name)
        except Exception:
            pattern = image_name

        image_found = _image_search(pattern, precision, in_region)
        if (image_found.x != -1) & (image_found.y != -1):
            return image_found
        else:
            raise FindError('Unable to find image %s' % image_name)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def findAll(what, precision=None, in_region=None):
    """Look for multiple matches of a Pattern or image

    :param what: String or Pattern
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return:
    """

    if isinstance(what, str) and _is_ocr_text(what):
        all_matches = _text_search_by(what, True, in_region, True)
        list_of_locations = []
        for match in all_matches:
            list_of_locations.append(Location(match['x'] + match['width'] / 2, match['y'] + match['height'] / 2))
        if len(list_of_locations) > 0:
            return list_of_locations
        else:
            raise FindError('Unable to find text %s' % what)

    elif isinstance(what, str) or isinstance(what, Pattern):
        try:
            pattern = Pattern(what)
        except Exception:
            pattern = what

        if precision is None:
            precision = Settings.MinSimilarity

        return _image_search_multiple(pattern, precision, in_region)
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def wait(image_name, timeout=None, precision=None, in_region=None):
    """Wait for a Pattern or image to appear

    :param image_name: String or Pattern
    :param timeout: Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if found
    """
    if isinstance(image_name, str) and _is_ocr_text(image_name):
        a_match = _text_search_by(image_name, True, in_region)
        if a_match is not None:
            return True
        else:
            raise FindError('Unable to find text %s' % image_name)

    elif isinstance(image_name, str) or isinstance(image_name, Pattern):
        if timeout is None:
            timeout = Settings.AutoWaitTimeout

        if precision is None:
            precision = Settings.MinSimilarity

        try:
            pattern = Pattern(image_name)
        except Exception:
            pattern = image_name

        image_found = _positive_image_search(pattern, timeout, precision, in_region)

        if image_found is not None:
            return True
        else:
            raise FindError('Unable to find image %s' % image_name)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def exists(pattern, timeout=None, precision=None, in_region=None):
    """Check if Pattern or image exists

    :param pattern: String or Pattern
    :param timeout: Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if found
    """

    if timeout is None:
        timeout = Settings.AutoWaitTimeout

    if precision is None:
        precision = Settings.MinSimilarity

    try:
        wait(pattern, timeout, precision, in_region)
        return True
    except FindError:
        return False


def waitVanish(image_name, timeout=None, precision=None, in_region=None):
    """Wait until a Pattern or image disappears

    :param image_name: Image, Pattern or string
    :param timeout:  Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if vanished
    """

    if timeout is None:
        timeout = Settings.AutoWaitTimeout

    if precision is None:
        precision = Settings.MinSimilarity

    pattern = Pattern(image_name)
    image_found = _negative_image_search(pattern, timeout, precision, in_region)

    if image_found is not None:
        return True
    else:
        raise FindError('%s did not vanish' % image_name)


def _click_pattern(pattern, clicks=None, duration=None, in_region=None, button=None):
    """Click on center or offset of a Pattern

    :param pattern: Input Pattern
    :param clicks: Number of mouse clicks
    :param duration: Speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3)
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    needle = cv2.imread(pattern.image_path)
    height, width, channels = needle.shape

    p_top = _positive_image_search(pattern=pattern, precision=Settings.MinSimilarity, region=in_region)

    if p_top is None:
        raise FindError('Unable to click on: %s' % pattern.image_path)

    possible_offset = pattern.getTargetOffset()

    if possible_offset is not None:
        _click_at(Location(p_top.x + possible_offset.x, p_top.y + possible_offset.y), clicks, duration, button)
    else:
        _click_at(Location(p_top.x + width / 2, p_top.y + height / 2), clicks, duration, button)


def _click_at(location=None, clicks=None, duration=None, button=None):
    """Click on Location coordinates

    :param location: Location , image name or Pattern
    :param clicks: Number of mouse clicks
    :param duration: speed of hovering from current location to target
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3)
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    if location is None:
        location = Location(0, 0)

    pyautogui.moveTo(location.x, location.y, duration)
    pyautogui.click(clicks=clicks, interval=Settings.ClickDelay, button=button)

    if Settings.ClickDelay != DEFAULT_CLICK_DELAY:
        Settings.ClickDelay = DEFAULT_CLICK_DELAY


def _general_click(where=None, clicks=None, duration=None, in_region=None, button=None):
    """General Mouse Click

    :param where: Location , image name or Pattern
    :param clicks: Number of mouse clicks
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3)
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    if isinstance(where, str) and _is_ocr_text(where):
        a_match = _text_search_by(where, True, in_region)
        if a_match is not None:
            click_location = Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
            _click_at(click_location, clicks, duration, button)

    elif isinstance(where, Location):
        _click_at(where, clicks, duration, button)

    elif isinstance(where, str) or isinstance(where, Pattern):
        try:
            pattern = Pattern(where)
        except Exception:
            pattern = where

        _click_pattern(pattern, clicks, duration, in_region, button)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def get_asset_img_size(of_what):
    """Get image size of asset image

    :param str || Pattern of_what: Image name or Pattern object
    :return: width, height as tuple
    """
    needle_path = None
    scale_factor = 1

    if isinstance(of_what, str):
        pattern = Pattern(of_what)
        needle_path = pattern.image_path
        scale_factor = pattern.scale_factor

    elif isinstance(of_what, Pattern):
        needle_path = of_what.image_path
        scale_factor = of_what.scale_factor

    needle = cv2.imread(needle_path)
    height, width, channels = needle.shape
    return int(width / scale_factor), int(height / scale_factor)


def click(where=None, duration=None, in_region=None):
    """Mouse left click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    _general_click(where, 1, duration, in_region, 'left')


def rightClick(where=None, duration=None, in_region=None):
    """Mouse right click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    _general_click(where, 1, duration, in_region, 'right')


def doubleClick(where=None, duration=None, in_region=None):
    """Mouse double click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    _general_click(where, 2, duration, in_region, 'left')


def _to_location(ps=None, in_region=None, align='top_left'):
    """Transform pattern or string to location

    :param ps: Pattern or string input
    :param in_region: Region object in order to minimize the area
    :param align: Alignment could be top_left, center
    :return: Location object
    """

    # TODO: Add multiple alignments if needed

    # TODO fix this (isinstance str or Pattern)

    if isinstance(ps, Location):
        return ps

    elif isinstance(Pattern(ps), Pattern):
        location = _image_search(Pattern(ps), Settings.MinSimilarity, in_region)
        if align == 'center':
            width, height = get_asset_img_size(Pattern(ps))
            return Location(location.getX() + width / 2, location.getY() + height / 2)
        else:
            return location


def dragDrop(drag_from, drop_to, duration=None):
    """Mouse drag and drop

    :param drag_from: Starting point for drag and drop. Can be pattern, string or location
    :param drop_to: Ending point for drag and drop. Can be pattern, string or location
    :param duration: speed of drag and drop
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    from_location = _to_location(ps=drag_from, align='center')
    to_location = _to_location(ps=drop_to, align='center')
    pyautogui.moveTo(from_location.x, from_location.y, 0)

    time.sleep(Settings.DelayBeforeMouseDown)
    pyautogui.mouseDown(button='left', _pause=False)

    time.sleep(Settings.DelayBeforeDrag)
    pyautogui._mouseMoveDrag('drag', to_location.x, to_location.y, 0, 0, duration, pyautogui.linear, 'left')

    time.sleep(Settings.DelayBeforeDrop)
    pyautogui.mouseUp(button='left', _pause=False)


def get_screen():
    """Returns full screen Image."""
    return Region(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


def keyDown(key):
    if isinstance(key, _IrisKey):
        pyautogui.keyDown(str(key))
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyDown(key)
        else:
            raise ValueError("Unsupported string input")
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def keyUp(key):
    if isinstance(key, _IrisKey):
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


class ZoomType(object):
    IN = 300 if Settings.isWindows() else 1
    OUT = -300 if Settings.isWindows() else -1


def zoom_with_mouse_wheel(nr_of_times=1, zoom_type=None):
    """Zoom in/Zoom out using the mouse wheel

    :param nr_of_times: Number of times the 'zoom in'/'zoom out' action should take place
    :param zoom_type: Type of the zoom action('zoom in'/'zoom out') intended to perform
    :return: None
    """

    # move focus in the middle of the page to be able to use the scroll
    pyautogui.moveTo(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2)
    for i in range(nr_of_times):
        if Settings.getOS() == Platform.MAC:
            pyautogui.keyDown('command')
        else:
            pyautogui.keyDown('ctrl')
        pyautogui.scroll(zoom_type)
        if Settings.getOS() == Platform.MAC:
            pyautogui.keyUp('command')
        else:
            pyautogui.keyUp('ctrl')
        time.sleep(0.5)
    pyautogui.moveTo(0, 0)


def paste(text):
    # load to clipboard
    pyperclip.copy(text)

    text_copied = False
    wait_scan_rate = float(Settings.WaitScanRate)
    interval = 1 / wait_scan_rate
    max_attempts = int(Settings.AutoWaitTimeout * wait_scan_rate)
    attempt = 0

    while not text_copied and attempt < max_attempts:
        if pyperclip.paste() == text:
            text_copied = True
        else:
            time.sleep(interval)
            attempt += 1

    if not text_copied:
        logger.error('Paste method failed')
        raise FindError

    if Settings.getOS() == Platform.MAC:
        type(text='v', modifier=KeyModifier.CMD)
    else:
        type(text='v', modifier=KeyModifier.CTRL)
    # clear clipboard
    pyperclip.copy('')


def type(text=None, modifier=None, interval=None):
    logger.debug('type method: ')
    if modifier is None:
        if isinstance(text, _IrisKey):
            logger.debug('Scenario 1: reserved key')
            logger.debug('Reserved key: %s' % text)
            pyautogui.keyDown(str(text))
            pyautogui.keyUp(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
        else:
            if interval is None:
                interval = Settings.TypeDelay

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
            pyautogui.keyDown(modifier_keys[0])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            pyautogui.keyDown(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            pyautogui.keyUp(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            pyautogui.keyUp(modifier_keys[0])
        elif num_keys == 2:
            pyautogui.keyDown(modifier_keys[0])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            pyautogui.keyDown(modifier_keys[1])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            pyautogui.keyDown(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            pyautogui.keyUp(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            pyautogui.keyUp(modifier_keys[1])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            pyautogui.keyUp(modifier_keys[0])
        else:
            logger.error('Returned key modifiers out of range')

    if Settings.TypeDelay != DEFAULT_TYPE_DELAY:
        Settings.TypeDelay = DEFAULT_TYPE_DELAY


def shutdown_process(process_name):
    if Settings.getOS() == Platform.WINDOWS:
        try:
            command = subprocess.Popen('taskkill /IM ' + process_name + '.exe', shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            logger.error('Command  failed: %s' % repr(e.command))
            raise Exception('Unable to run Command')
    elif Settings.getOS() == Platform.MAC or Settings.getOS() == Platform.LINUX:
        try:
            command = subprocess.Popen('pkill ' + process_name, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            logger.error('Command  failed: %s' % repr(e.command))
            raise Exception('Unable to run Command')
