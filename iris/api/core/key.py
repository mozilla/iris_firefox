# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import ctypes
import logging
import subprocess
import time

import pyautogui
import pyperclip

from errors import FindError
from platform import Platform
from settings import Settings, DEFAULT_TYPE_DELAY
from util.core_helper import INVALID_GENERIC_INPUT, IrisCore
from util.parse_args import parse_args

DEFAULT_KEY_SHORTCUT_DELAY = 0.1

logger = logging.getLogger(__name__)


class _IrisKey(object):

    def __init__(self, label, value=None, reserved=True):
        """Function assign values to the 'label', 'value' and 'is_reserved' parameters."""

        """Key label."""
        self.label = label

        """Key value."""
        self.value = value

        """Boolean property."""
        self.is_reserved = reserved

    def __str__(self):
        """Function returns the 'label' parameter."""
        return self.label


class Key(object):
    """Class with multiple instances of the _IrisKey class."""

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

    """Additional keys."""
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
    def is_lock_on(keyboard_key):
        """Static method which determines if a keyboard key(CAPS LOCK, NUM LOCK or SCROLL LOCK) is ON.

        :param keyboard_key: Keyboard key(CAPS LOCK, NUM LOCK or SCROLL LOCK).
        :return: TRUE if keyboard_key state is ON or FALSE if keyboard_key state is OFF.
        """
        if Settings.get_os() == Platform.WINDOWS:
            hll_dll = ctypes.WinDLL("User32.dll")
            keyboard_code = 0
            if keyboard_key == Key.CAPS_LOCK:
                keyboard_code = 0x14
            elif keyboard_key == Key.NUM_LOCK:
                keyboard_code = 0x90
            elif keyboard_key == Key.SCROLL_LOCK:
                keyboard_code = 0x91
            try:
                key_state = hll_dll.GetKeyState(keyboard_code) & 1
            except Exception:
                raise Exception('Unable to run Command.')
            if key_state == 1:
                return True
            else:
                return False
        elif Settings.get_os() == Platform.LINUX or Settings.get_os() == Platform.MAC:
            try:
                cmd = subprocess.Popen('xset q', shell=True, stdout=subprocess.PIPE)
                IrisCore.shutdown_process('Xquartz')
            except subprocess.CalledProcessError as e:
                logger.error('Command  failed: %s' % repr(e.cmd))
                raise Exception('Unable to run Command.')
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

class KeyModifier(object):

    """Keyboard key variables."""
    SHIFT = Key.SHIFT.value
    CTRL = Key.CTRL.value
    CMD = Key.CMD.value
    WIN = Key.WIN.value
    META = Key.META.value
    ALT = Key.ALT.value

    @staticmethod
    def get_active_modifiers(value):
        """Gets all the active modifiers depending on the used OS.

        :param value: Key modifier.
        :return: Returns an array with all the active modifiers.
        """
        all_modifiers = [
            Key.SHIFT,
            Key.CTRL]
        if Settings.get_os() == Platform.MAC:
            all_modifiers.append(Key.CMD)
        elif Settings.get_os() == Platform.WINDOWS:
            all_modifiers.append(Key.WIN)
        else:
            all_modifiers.append(Key.META)

        all_modifiers.append(Key.ALT)

        active_modifiers = []
        for item in all_modifiers:
            if item.value & value:
                active_modifiers.append(item.label)
        return active_modifiers


def key_down(key):
    """Performs a keyboard key press without the release. This will put that key in a held down state.

    :param key: The key to be pressed down.
    :return: None.
    """
    if isinstance(key, _IrisKey):
        pyautogui.keyDown(str(key))
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyDown(key)
        else:
            raise ValueError("Unsupported string input.")
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def key_up(key):
    """Performs a keyboard key release (without the press down beforehand).

    :param key: The key to be released up.
    :return: None.
    """
    if isinstance(key, _IrisKey):
        pyautogui.keyUp(str(key))
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyUp(key)
        else:
            raise ValueError("Unsupported string input.")
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def type(text=None, modifier=None, interval=None):
    """
    :param str || list text: If a string, then the characters to be pressed. If a list, then the key names of the keys
                             to press in order.
    :param modifier: Key modifier.
    :param interval: The number of seconds in between each press. By default it is 0 seconds.
    :return: None.
    """
    logger.debug('type method: ')
    if modifier is None:
        if isinstance(text, _IrisKey):
            logger.debug('Scenario 1: reserved key.')
            logger.debug('Reserved key: %s' % text)
            pyautogui.keyDown(str(text))
            pyautogui.keyUp(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
        else:
            if interval is None:
                interval = Settings.type_delay

            logger.debug('Scenario 2: normal key or text block.')
            logger.debug('Text: %s' % text)
            pyautogui.typewrite(text, interval)
    else:
        logger.debug('Scenario 3: combination of modifiers and other keys.')
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
            logger.error('Returned key modifiers out of range.')

    if Settings.type_delay != DEFAULT_TYPE_DELAY:
        Settings.type_delay = DEFAULT_TYPE_DELAY


def paste(text):
    """
    :param text: Text to be pasted.
    :return: None.
    """

    # Load text to clipboard.
    pyperclip.copy(text)

    text_copied = False
    wait_scan_rate = float(Settings.wait_scan_rate)
    interval = 1 / wait_scan_rate
    max_attempts = int(Settings.auto_wait_timeout * wait_scan_rate)
    attempt = 0

    while not text_copied and attempt < max_attempts:
        if pyperclip.paste() == text:
            text_copied = True
        else:
            time.sleep(interval)
            attempt += 1

    if not text_copied:
        raise FindError('Paste method failed.')

    if Settings.get_os() == Platform.MAC:
        type(text='v', modifier=KeyModifier.CMD)
    else:
        type(text='v', modifier=KeyModifier.CTRL)

    # Clear clipboard.
    pyperclip.copy('')


def check_keyboard_state():
    """Check Keyboard state.

    Iris cannot run in case Key.CAPS_LOCK, Key.NUM_LOCK or Key.SCROLL_LOCK are pressed.
    """
    if parse_args().no_check:
        return True

    key_on = False
    keyboard_keys = [Key.CAPS_LOCK, Key.NUM_LOCK, Key.SCROLL_LOCK]
    for key in keyboard_keys:
        if Key.is_lock_on(key):
            logger.error('Cannot run Iris because %s is on. Please turn it off to continue.' % str(key).upper())
            key_on = True
    return not key_on
