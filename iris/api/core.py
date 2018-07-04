# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import Queue
import copy
import ctypes
import inspect
import multiprocessing
import platform
import re
import subprocess
import time
from datetime import datetime

import pyautogui
import pyperclip
import pytesseract

from errors import *
from helpers.image_remove_noise import process_image_for_ocr, OCR_IMAGE_SIZE
from helpers.parse_args import parse_args
from iris.api.helpers.iris_image import *

try:
    import Image
except ImportError:
    from PIL import Image

args = parse_args()

pyautogui.FAILSAFE = False
save_debug_images = args.level == 10

INVALID_GENERIC_INPUT = 'Invalid input'
INVALID_NUMERIC_INPUT = 'Expected numeric value'

DEFAULT_MIN_SIMILARITY = 0.8
DEFAULT_SLOW_MOTION_DELAY = 2
DEFAULT_MOVE_MOUSE_DELAY = args.mouse
DEFAULT_OBSERVE_MIN_CHANGED_PIXELS = 50
DEFAULT_TYPE_DELAY = 0
DEFAULT_CLICK_DELAY = 0
DEFAULT_WAIT_SCAN_RATE = 3
DEFAULT_OBSERVE_SCAN_RATE = 3
DEFAULT_AUTO_WAIT_TIMEOUT = 3
DEFAULT_DELAY_BEFORE_MOUSE_DOWN = 0.3
DEFAULT_DELAY_BEFORE_DRAG = 0.3
DEFAULT_DELAY_BEFORE_DROP = 0.3
DEFAULT_KEY_SHORTCUT_DELAY = 0.1

MIN_CPU_FOR_MULTIPROCESSING = 4

_images = {}

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


def get_os():
    """Get the type of the operating system your script is running on."""
    current_system = platform.system()
    current_os = ''
    if current_system == 'Windows':
        current_os = 'win'
    elif current_system == 'Linux':
        current_os = 'linux'
    elif current_system == 'Darwin':
        current_os = 'osx'
    else:
        logger.error('Iris does not yet support your current environment: ' + current_system)

    return current_os


def get_platform():
    return platform.machine()


def get_os_version():
    """Get the version string of the operating system your script is running on."""
    return platform.release()


def get_module_dir():
    return os.path.realpath(os.path.split(__file__)[0] + '/../..')


current_platform_pattern = os.path.join('images', get_os())
PROJECT_BASE_PATH = get_module_dir()


def load_all_patterns():
    duplicate_images = ''
    for root, dirs, files in os.walk(PROJECT_BASE_PATH):
        for file_name in files:
            if file_name.endswith('.png'):
                if current_platform_pattern in root or 'common' in root or 'local_web' in root:
                    new_image = IrisImage(file_name, root)
                    if new_image.name in _images:
                        new_file = os.path.join(root, file_name)
                        duplicate_images += '\n"%s" - "%s"' % (_images[new_image.name].path, new_file)
                    else:
                        _images[new_image.name] = new_image
    if len(duplicate_images) > 0:
        logger.warning('Found multiple images with the same name:\n%s' % str(duplicate_images))


"""
pyautogui.size() works correctly everywhere except Mac Retina
This technique works everywhere, so we'll use it instead
"""

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


class _IrisSettings(object):
    _wait_scan_rate = DEFAULT_WAIT_SCAN_RATE
    _type_delay = DEFAULT_TYPE_DELAY
    _move_mouse_delay = DEFAULT_MOVE_MOUSE_DELAY
    _click_delay = DEFAULT_CLICK_DELAY
    _min_similarity = DEFAULT_MIN_SIMILARITY
    _auto_wait_timeout = DEFAULT_AUTO_WAIT_TIMEOUT
    _delay_before_mouse_down = DEFAULT_DELAY_BEFORE_MOUSE_DOWN
    _delay_before_drag = DEFAULT_DELAY_BEFORE_DRAG
    _delay_before_drop = DEFAULT_DELAY_BEFORE_DROP
    _slow_motion_delay = DEFAULT_SLOW_MOTION_DELAY
    _observe_scan_rate = DEFAULT_OBSERVE_SCAN_RATE
    _observe_min_changed_pixels = DEFAULT_OBSERVE_MIN_CHANGED_PIXELS

    def __init__(self):
        self._wait_scan_rate = self.WaitScanRate
        self._type_delay = self.TypeDelay
        self._move_mouse_delay = self.MoveMouseDelay
        self._click_delay = self.ClickDelay
        self._min_similarity = self.MinSimilarity
        self._auto_wait_timeout = self.AutoWaitTimeout
        self._delay_before_mouse_down = self.DelayBeforeMouseDown
        self._delay_before_drag = self.DelayBeforeDrag
        self._delay_before_drop = self.DelayBeforeDrop
        self._slow_motion_delay = self.SlowMotionDelay
        self._observe_scan_rate = self.ObserveScanRate
        self._observe_min_changed_pixels = self.ObserveMinChangedPixels

    @property
    def WaitScanRate(self):
        return self._wait_scan_rate

    @WaitScanRate.setter
    def WaitScanRate(self, value):
        self._wait_scan_rate = value

    @property
    def TypeDelay(self):
        return self._type_delay

    @TypeDelay.setter
    def TypeDelay(self, value):
        if value > 1:
            self._type_delay = 1
        else:
            self._type_delay = value

    @property
    def MoveMouseDelay(self):
        return self._move_mouse_delay

    @MoveMouseDelay.setter
    def MoveMouseDelay(self, value):
        self._move_mouse_delay = value

    @property
    def ClickDelay(self):
        return self._click_delay

    @ClickDelay.setter
    def ClickDelay(self, value):
        if value > 1:
            self._click_delay = 1
        else:
            self._click_delay = value

    @property
    def MinSimilarity(self):
        return self._min_similarity

    @MinSimilarity.setter
    def MinSimilarity(self, value):
        if value > 1:
            self._min_similarity = 1
        else:
            self._min_similarity = value

    @property
    def AutoWaitTimeout(self):
        return self._auto_wait_timeout

    @AutoWaitTimeout.setter
    def AutoWaitTimeout(self, value):
        self._auto_wait_timeout = value

    @property
    def DelayBeforeMouseDown(self):
        return self._delay_before_mouse_down

    @DelayBeforeMouseDown.setter
    def DelayBeforeMouseDown(self, value):
        self._delay_before_mouse_down = value

    @property
    def DelayBeforeDrag(self):
        return self._delay_before_drag

    @DelayBeforeDrag.setter
    def DelayBeforeDrag(self, value):
        self._delay_before_drag = value

    @property
    def DelayBeforeDrop(self):
        return self._delay_before_drop

    @DelayBeforeDrop.setter
    def DelayBeforeDrop(self, value):
        self._delay_before_drop = value

    @property
    def SlowMotionDelay(self):
        return self._slow_motion_delay

    @SlowMotionDelay.setter
    def SlowMotionDelay(self, value):
        self._slow_motion_delay = value

    @property
    def ObserveScanRate(self):
        return self._observe_scan_rate

    @ObserveScanRate.setter
    def ObserveScanRate(self, value):
        self._observe_scan_rate = value

    @property
    def ObserveMinChangedPixels(self):
        return self._observe_min_changed_pixels

    @ObserveMinChangedPixels.setter
    def ObserveMinChangedPixels(self, value):
        self._observe_min_changed_pixels = value

    @property
    def ActionLogs(self):
        raise UnsupportedAttributeError('Unsupported attribute Settings.ActionLogs')

    @ActionLogs.setter
    def ActionLogs(self, value):
        raise UnsupportedAttributeError('Unsupported attribute Settings.ActionLogs')

    @property
    def DebugLogs(self):
        raise UnsupportedAttributeError('Unsupported attribute Settings.DebugLogs')

    @DebugLogs.setter
    def DebugLogs(self, value):
        raise UnsupportedAttributeError('Unsupported attribute Settings.DebugLogs')

    @property
    def InfoLogs(self):
        raise UnsupportedAttributeError('Unsupported attribute Settings.InfoLogs')

    @InfoLogs.setter
    def InfoLogs(self, value):
        raise UnsupportedAttributeError('Unsupported attribute Settings.InfoLogs')

    @staticmethod
    def getSikuliVersion():
        raise UnsupportedMethodError('Unsupported method Settings.getSikuliVersion()')

    @staticmethod
    def getOS():
        """Get the type of the operating system your script is running on."""
        return get_os()

    @staticmethod
    def getOSVersion():
        """Get the version string of the operating system your script is running on."""
        return get_os_version()

    @staticmethod
    def isLinux():
        """Checks if we are running on a Linux system.

        :return: True if we are running on a Linux system, False otherwise
        """
        return get_os() == Platform.LINUX

    @staticmethod
    def isMac():
        """Checks if we are running on a Mac system.

        :return: True if we are running on a Mac system, False otherwise
        """
        return get_os() == Platform.MAC

    @staticmethod
    def isWindows():
        """Checks if we are running on a Windows system.

        :return: True if we are running on a Windows system, False otherwise
        """
        return get_os() == Platform.WINDOWS


Settings = _IrisSettings()


class Env(object):
    @staticmethod
    def getClipboard():
        return pyperclip.paste()

    @staticmethod
    def isLockOn():
        raise UnsupportedMethodError('Unsupported method Env.isLockOn(). Use Key.isLockOn() instead.')

    @staticmethod
    def getOSVersion():
        raise UnsupportedMethodError('Unsupported method Env.getOSVersion(). Use Settings.getOSVersion() instead.')

    @staticmethod
    def getOS():
        raise UnsupportedMethodError('Unsupported method Env.getOS(). Use Settings.getOS() instead.')

    @staticmethod
    def getMouseLocation():
        raise UnsupportedMethodError('Unsupported method Env.getMouseLocation(). Use Mouse.at() instead.')

    @staticmethod
    def addHotkey():
        raise UnsupportedMethodError('Unsupported method Env.addHotkey().')

    @staticmethod
    def removeHotkey():
        raise UnsupportedMethodError('Unsupported method Env.removeHotkey().')

    @staticmethod
    def getSikuliVersion():
        raise UnsupportedMethodError('Unsupported method Env.getSikuliVersion().')


class Sikulix(object):
    @staticmethod
    def prefLoad():
        raise UnsupportedMethodError('Unsupported method Sikulix.prefLoad().')

    @staticmethod
    def prefRemove():
        raise UnsupportedMethodError('Unsupported method Sikulix.prefRemove().')

    @staticmethod
    def prefStore():
        raise UnsupportedMethodError('Unsupported method Sikulix.prefStore().')


class App(object):
    def __init__(self):
        self.open = self._instance_open_app
        self.focus = self._instance_focus_app
        self.close = self._instance_close_app

    @staticmethod
    def open(application):
        raise UnsupportedClassMethodError('Unsupported classmethod App.open(application).')

    def _instance_open_app(self, waitTime=1):
        raise UnsupportedMethodError('Unsupported method App.open([waitTime]).')

    @staticmethod
    def focus(application):
        raise UnsupportedClassMethodError('Unsupported classmethod App.focus(application).')

    def _instance_focus_app(self):
        raise UnsupportedMethodError('Unsupported method App.focus().')

    @staticmethod
    def close(application):
        raise UnsupportedClassMethodError('Unsupported classmethod App.close(application).')

    def _instance_close_app(self):
        raise UnsupportedMethodError('Unsupported method App.close().')

    @staticmethod
    def pause(waitTime):
        raise UnsupportedClassMethodError('Unsupported classmethod App.pause(waitTime).')

    def isRunning(self):
        raise UnsupportedMethodError('Unsupported method App.isRunning().')

    def hasWindow(self):
        raise UnsupportedMethodError('Unsupported method App.hasWindow().')

    def getWindow(self):
        raise UnsupportedMethodError('Unsupported method App.getWindow().')

    def getPID(self):
        raise UnsupportedMethodError('Unsupported method App.getPID().')

    def getName(self):
        raise UnsupportedMethodError('Unsupported method App.getName().')

    def setUsing(self, parametertext):
        raise UnsupportedMethodError('Unsupported method App.setUsing(parametertext).')

    @staticmethod
    def focusedWindow():
        raise UnsupportedClassMethodError('Unsupported classmethod App.focusedWindow().')

    def window(self, n=1):
        raise UnsupportedMethodError('Unsupported method App.window([n]).')

    @staticmethod
    def getClipboard():
        raise UnsupportedMethodError('Unsupported method App.getClipboard().')


class Guide(object):
    @staticmethod
    def rectangle(element):
        raise UnsupportedMethodError('Unsupported method Guide.rectangle(element).')

    @staticmethod
    def circle(element):
        raise UnsupportedMethodError('Unsupported method Guide.circle(element).')

    @staticmethod
    def text(element, txt):
        raise UnsupportedMethodError('Unsupported method Guide.text(element, txt).')

    @staticmethod
    def tooltip(element, txt):
        raise UnsupportedMethodError('Unsupported method Guide.tooltip(element, txt).')

    @staticmethod
    def button(element, name):
        raise UnsupportedMethodError('Unsupported method Guide.button(element, name).')

    @staticmethod
    def show(seconds=1):
        raise UnsupportedMethodError('Unsupported method Guide.show([seconds]).')


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


class Pattern(object):
    def __init__(self, image_name):
        self.image_name = image_name
        self.image_path = _images[self.image_name].path
        self.scale_factor = _images[self.image_name].scale_factor
        self.target_offset = None

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


class Vision(object):
    def __init__(self):
        pass

    @staticmethod
    def getParameter():
        raise UnsupportedMethodError('Unsupported method Vision.getParameter()')

    @staticmethod
    def setParameter():
        raise UnsupportedMethodError('Unsupported method Vision.setParameter()')


class Do(object):
    def __init__(self):
        pass

    @staticmethod
    def input():
        raise UnsupportedMethodError('Unsupported method Do.input()')

    @staticmethod
    def popAsk():
        raise UnsupportedMethodError('Unsupported method Do.popAsk()')

    @staticmethod
    def popError():
        raise UnsupportedMethodError('Unsupported method Do.popError()')

    @staticmethod
    def popup():
        raise UnsupportedMethodError('Unsupported method Do.popup()')


class Platform(object):
    """Class that holds all supported operating systems (HIDEF = High definition displays)."""
    WINDOWS = 'win'
    LINUX = 'linux'
    MAC = 'osx'
    ALL = Settings.getOS()
    HIDEF = not (pyautogui.screenshot().size == pyautogui.size())
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    LOWRES = (SCREEN_WIDTH < 1280 or SCREEN_HEIGHT < 800)


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

    :param IrisImage needle: Image details (needle)
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

    :param IrisImage needle:  Image details (needle)
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


def _add_positive_image_search_result_in_queue(queue, image_name, precision=None, region=None, all_images=None):
    """Puts result in a queue if image is found

    :param Queue.Queue queue: Queue where the result of the search is added
    :param str image_name: name of the searched image
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :param dict all_images: hold the list of all images that are loaded into the tests
    :return:
    """

    if precision is None:
        precision = Settings.MinSimilarity

    result = _image_search(all_images[image_name], precision, region)
    if result.getX() != -1:
        queue.put(result)


def _add_negative_image_search_result_in_queue(queue, image_name, precision=None, region=None, all_images=None):
    """Puts result in a queue if image is NOT found

    :param Queue.Queue queue: Queue where the result of the search is added
    :param str image_name: name of the searched image
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :param dict all_images: hold the list of all images that are loaded into the tests
    :return:
    """

    if precision is None:
        precision = Settings.MinSimilarity

    result = _image_search(all_images[image_name], precision, region)
    if result.getX() == -1:
        queue.put(result)


def _image_search(image_details, precision=None, region=None):
    """ Wrapper over _match_template. Search image in a Region or full screen

    :param IrisImage image_details: Image details (needle)
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """

    if precision is None:
        precision = Settings.MinSimilarity

    stack_image = _region_grabber(region=region)
    location = _match_template(image_details, stack_image, precision)

    if location.x == -1 or location.y == -1:
        return location
    elif region is not None:
        return Location(location.x + region.x, location.y + region.y)
    else:
        return location


def _image_search_multiple(image_details, precision=None, region=None):
    """ Wrapper over _match_template_multiple. Search image (multiple) in a Region or full screen

    :param IrisImage image_details: Image details (needle)
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: List[Location]
    """

    if precision is None:
        precision = Settings.MinSimilarity

    stack_image = _region_grabber(region=region)
    return _match_template_multiple(image_details, stack_image, precision)


def _calculate_interval_max_attempts(timeout=None):
    if timeout is None:
        timeout = Settings.AutoWaitTimeout

    wait_scan_rate = float(Settings.WaitScanRate)
    interval = 1 / wait_scan_rate
    max_attempts = int(timeout * wait_scan_rate)
    return interval, max_attempts


def _positive_image_search_loop(image_name, timeout=None, precision=None, region=None):
    """ Search for an image (in loop) in a Region or full screen

    :param str image_name: name of the searched image
    :param timeout: Number as maximum waiting time in seconds.
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    if precision is None:
        precision = Settings.MinSimilarity

    image_details = _images[image_name]
    pos = _image_search(image_details, precision, region)
    tries = 0
    while pos.getX() == -1 and tries < max_attempts:
        logger.debug("Searching for image %s" % image_name)
        time.sleep(interval)
        pos = _image_search(image_details, precision, region)
        tries += 1

    return None if pos.getX() == -1 else pos


def _positive_image_search_multiprocess(image_name, timeout=None, precision=None, region=None):
    """Checks if image is found using multiprocessing

    :param str image_name: name of the searched image
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
                                    args=(out_q, image_name, precision, region, _images))
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


def _positive_image_search(image_name, timeout=None, precision=None, region=None):
    if use_multiprocessing():
        return _positive_image_search_multiprocess(image_name, timeout, precision, region)
    else:
        return _positive_image_search_loop(image_name, timeout, precision, region)


def _negative_image_search_loop(image_name, timeout=None, precision=None, region=None):
    """ Search if an image (in loop) is NOT in a Region or full screen

    :param str image_name: name of the searched image
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
    image_name = _get_pattern_name(image_name)
    image_details = _images[image_name]

    while pattern_found is True and tries < max_attempts:
        image_found = _image_search(image_details, precision, region)
        if (image_found.x != -1) & (image_found.y != -1):
            pattern_found = True
        else:
            pattern_found = False
        tries += 1
        time.sleep(interval)

    return None if pattern_found else True


def _negative_image_search_multiprocess(image_name, timeout=None, precision=None, region=None):
    """Checks if image is NOT found or it vanished using multiprocessing

    :param str image_name: name of the searched image
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
                                    args=(out_q, image_name, precision, region, _images))
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


def _negative_image_search(image_name, timeout=None, precision=None, region=None):
    if use_multiprocessing():
        return _negative_image_search_multiprocess(image_name, timeout, precision, region)
    else:
        return _negative_image_search_loop(image_name, timeout, precision, region)


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


def _get_pattern_name(string_or_pattern):
    """ Helper for getting image path

    :param str || Pattern string_or_pattern: Image name or Pattern object
    :return: string of image path
    """
    if isinstance(string_or_pattern, Pattern):
        return string_or_pattern.image_name
    elif isinstance(string_or_pattern, str):
        if string_or_pattern in _images:
            return _images[string_or_pattern].name
        else:
            raise ValueError('Unknown image name: %s' % string_or_pattern)
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


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
        image_name = _get_pattern_name(where)
        pos = _image_search(_images[image_name], region=in_region)
        if pos.x is not -1:
            needle_width, needle_height = get_asset_img_size(image_name)
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
            raise FindError('Unable to find image %s' % image_name)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def find(what, precision=None, in_region=None):
    """Look for a single match of a Pattern or image

    :param what: String or Pattern
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: Location
    """
    if isinstance(what, str) and _is_ocr_text(what):
        a_match = _text_search_by(what, True, in_region)
        if a_match is not None:
            return Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        else:
            raise FindError('Unable to find text %s' % what)

    elif isinstance(what, str) or isinstance(what, Pattern):

        if what not in _images:
            return ValueError("Unable to locate %s image in project" % what)

        if precision is None:
            precision = Settings.MinSimilarity

        image_name = _get_pattern_name(what)
        image_found = _image_search(_images[image_name], precision, in_region)
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

        if precision is None:
            precision = Settings.MinSimilarity

        image_name = _get_pattern_name(what)
        return _image_search_multiple(image_name, precision, in_region)
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def wait(for_what, timeout=None, precision=None, in_region=None):
    """Wait for a Pattern or image to appear

    :param for_what: String or Pattern
    :param timeout: Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if found
    """

    if isinstance(for_what, str) and _is_ocr_text(for_what):
        a_match = _text_search_by(for_what, True, in_region)
        if a_match is not None:
            return True
        else:
            raise FindError('Unable to find text %s' % for_what)

    elif isinstance(for_what, str) or isinstance(for_what, Pattern):

        if timeout is None:
            timeout = Settings.AutoWaitTimeout

        if precision is None:
            precision = Settings.MinSimilarity

        image_name = _get_pattern_name(for_what)
        image_found = _positive_image_search(image_name, timeout, precision, in_region)

        if image_found is not None:
            return True
        else:
            raise FindError('Unable to find image %s' % image_name)
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def exists(what, timeout=None, precision=None, in_region=None):
    """Check if Pattern or image exists

    :param what: String or Pattern
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
        wait(what, timeout, precision, in_region)
        return True
    except FindError:
        return False


def waitVanish(for_what, timeout=None, precision=None, in_region=None):
    """Wait until a Pattern or image disappears

    :param for_what: Image, Pattern or string
    :param timeout:  Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if vanished
    """

    if timeout is None:
        timeout = Settings.AutoWaitTimeout

    if precision is None:
        precision = Settings.MinSimilarity

    image_name = _get_pattern_name(for_what)
    image_found = _negative_image_search(image_name, timeout, precision, in_region)

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

    p_top = _positive_image_search(image_name=pattern.image_name, precision=Settings.MinSimilarity, region=in_region)

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

    elif isinstance(where, str):
        pattern = Pattern(where)
        _click_pattern(pattern, clicks, duration, in_region, button)

    elif isinstance(where, Pattern):
        _click_pattern(where, clicks, duration, in_region, button)

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

    if isinstance(ps, Pattern):
        location = _image_search(_images[ps.image_name], Settings.MinSimilarity, in_region)
        if align == 'center':
            width, height = get_asset_img_size(_images[ps.image_name])
            return Location(location.getX() + width / 2, location.getY() + height / 2)
        else:
            return location

    elif isinstance(ps, str):
        location = _image_search(_images[ps], Settings.MinSimilarity, in_region)
        if align == 'center':
            width, height = get_asset_img_size(ps)
            return Location(location.getX() + width / 2, location.getY() + height / 2)
        else:
            return location

    elif isinstance(ps, Location):
        return ps


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


class ZoomType:
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
