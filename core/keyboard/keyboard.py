# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import ctypes
import logging
import subprocess
import time

import pyautogui
import pyperclip as pyperclip

from core.arg_parser import parse_args
from core.enums import OSPlatform
from core.errors import FindError
from core.settings import Settings

DEFAULT_KEY_SHORTCUT_DELAY = 0.1

logger = logging.getLogger(__name__)


class _IrisKey(object):

    def __init__(self, label: str, value: int = None, x11key=None, reserved=True):
        """Function assign values to the 'label', 'value' and 'is_reserved' parameters."""

        """Key label."""
        self.label = label

        """Key value."""
        self.value = value

        """Key x11 value."""
        self.x11key = x11key

        """Boolean property."""
        self.is_reserved = reserved

    def __str__(self):
        """Function returns the 'label' parameter."""
        return self.label


class Key(object):
    """Class with multiple instances of the _IrisKey class."""

    ADD = _IrisKey('add', None, 'KP_Add')
    ALT = _IrisKey('alt', 1 << 3, 'Alt_L')
    BACKSPACE = _IrisKey('backspace', None, 'BackSpace')
    CAPS_LOCK = _IrisKey('capslock', None, 'Caps_Lock')
    CMD = _IrisKey('command', 1 << 2)
    CTRL = _IrisKey('ctrl', 1 << 1, 'Control_L')
    DELETE = _IrisKey('del', None, 'Delete')
    DIVIDE = _IrisKey('divide', None, 'KP_Divide')
    DOWN = _IrisKey('down', None, 'Down')
    ENTER = ('\n', None, 'Return')
    END = _IrisKey('end', None, 'End')
    ESC = _IrisKey('esc', None, 'Escape')
    F1 = _IrisKey('f1', None, 'F1')
    F2 = _IrisKey('f2', None, 'F2')
    F3 = _IrisKey('f3', None, 'F3')
    F4 = _IrisKey('f4', None, 'F4')
    F5 = _IrisKey('f5', None, 'F5')
    F6 = _IrisKey('f6', None, 'F6')
    F7 = _IrisKey('f7', None, 'F7')
    F8 = _IrisKey('f8', None, 'F8')
    F9 = _IrisKey('f9', None, 'F9')
    F10 = _IrisKey('f10', None, 'F10')
    F11 = _IrisKey('f11', None, 'F11')
    F12 = _IrisKey('f12', None, 'F12')
    F13 = _IrisKey('f13', None, 'F13')
    F14 = _IrisKey('f14', None, 'F14')
    F15 = _IrisKey('f15', None, 'F15')
    HOME = _IrisKey('home', None, 'Home')
    INSERT = _IrisKey('insert', None, 'Insert')
    LEFT = _IrisKey('left', None, 'Left')
    META = _IrisKey('winleft', 1 << 2)
    MINUS = _IrisKey('subtract', None)
    MULTIPLY = _IrisKey('multiply', None, 'KP_Multiply')
    NUM0 = _IrisKey('num0', None, 'KP_0')
    NUM1 = _IrisKey('num1', None, 'KP_1')
    NUM2 = _IrisKey('num2', None, 'KP_2')
    NUM3 = _IrisKey('num3', None, 'KP_3')
    NUM4 = _IrisKey('num4', None, 'KP_4')
    NUM5 = _IrisKey('num5', None, 'KP_5')
    NUM6 = _IrisKey('num6', None, 'KP_6')
    NUM7 = _IrisKey('num7', None, 'KP_7')
    NUM8 = _IrisKey('num8', None, 'KP_8')
    NUM9 = _IrisKey('num9', None, 'KP_9')
    NUM_LOCK = _IrisKey('numlock', None, 'Num_Lock')
    PAGE_DOWN = _IrisKey('pagedown', None, 'Page_Down')
    PAGE_UP = _IrisKey('pageup', None, 'Page_Up')
    PAUSE = _IrisKey('pause', None, 'Pause')
    PRINT_SCREEN = _IrisKey('printscreen', None, 'Print')
    RIGHT = _IrisKey('right', None, 'Right')
    SCROLL_LOCK = _IrisKey('scrolllock', None, 'Scroll_Lock')
    SEPARATOR = _IrisKey('separator', None, 'KP_Separator')
    SHIFT = _IrisKey('shift', 1 << 0, 'Shift_L')
    SPACE = (' ', None, 'space')
    TAB = ('\t', None, 'Tab')
    UP = _IrisKey('up', None, 'Up')
    WIN = _IrisKey('win', 1 << 2)

    """Additional keys."""
    ACCEPT = _IrisKey('accept', None)
    ALT_LEFT = _IrisKey('altleft', None, 'Alt_L')
    ALT_RIGHT = _IrisKey('altright', None, 'Alt_R')
    APPS = _IrisKey('apps', None, 'Super_L')
    BROWSER_BACK = _IrisKey('browserback', None)
    BROWSER_FAVORITES = _IrisKey('browserfavorites', None)
    BROWSER_FORWARD = _IrisKey('browserforward', None)
    BROWSER_HOME = _IrisKey('browserhome', None)
    BROWSER_REFRESH = _IrisKey('browserrefresh', None)
    BROWSER_SEARCH = _IrisKey('browsersearch', None)
    BROWSER_STOP = _IrisKey('browserstop', None)
    CLEAR = _IrisKey('clear', None)
    COMMAND = _IrisKey('command', None)
    CONVERT = _IrisKey('convert', None)
    CTRL_LEFT = _IrisKey('ctrlleft', None, 'Control_L')
    CTRL_RIGHT = _IrisKey('ctrlright', None, 'Control_R')
    DECIMAL = _IrisKey('decimal', None, 'KP_Decimal')
    EXECUTE = _IrisKey('execute', None, 'Execute')
    F16 = _IrisKey('f16', None, 'F16')
    F17 = _IrisKey('f17', None, 'F17')
    F18 = _IrisKey('f18', None, 'F18')
    F19 = _IrisKey('f19', None, 'F19')
    F20 = _IrisKey('f20', None, 'F20')
    F21 = _IrisKey('f21', None, 'F21')
    F22 = _IrisKey('f22', None, 'F22')
    F23 = _IrisKey('f23', None, 'F23')
    F24 = _IrisKey('f24', None, 'F24')
    FINAL = _IrisKey('final', None)
    FN = _IrisKey('fn', None)
    HANGUEL = _IrisKey('hanguel', None)
    HANGUL = _IrisKey('hangul', None)
    HANJA = _IrisKey('hanja', None)
    HELP = _IrisKey('help', None, 'Help')
    JUNJA = _IrisKey('junja', None)
    KANA = _IrisKey('kana', None)
    KANJI = _IrisKey('kanji', None)
    LAUNCH_APP1 = _IrisKey('launchapp1', None)
    LAUNCH_APP2 = _IrisKey('launchapp2', None)
    LAUNCH_MAIL = _IrisKey('launchmail', None)
    LAUNCH_MEDIA_SELECT = _IrisKey('launchmediaselect', None)
    MODE_CHANGE = _IrisKey('modechange', None)
    NEXT_TRACK = _IrisKey('nexttrack', None)
    NONCONVERT = _IrisKey('nonconvert', None)
    OPTION = _IrisKey('option', None)
    OPTION_LEFT = _IrisKey('optionleft', None)
    OPTION_RIGHT = _IrisKey('optionright', None)
    PGDN = _IrisKey('pgdn', None)
    PGUP = _IrisKey('pgup', None)
    PLAY_PAUSE = _IrisKey('playpause', None)
    PREV_TRACK = _IrisKey('prevtrack', None)
    PRINT = _IrisKey('print', None, 'Print')
    PRNT_SCRN = _IrisKey('prntscrn', None, 'Print')
    PRTSC = _IrisKey('prtsc', None)
    PRTSCR = _IrisKey('prtscr', None)
    RETURN = _IrisKey('return', None)
    SELECT = _IrisKey('select', None, 'Select')
    SHIFT_LEFT = _IrisKey('shiftleft', None, 'Shift_L')
    SHIFT_RIGHT = _IrisKey('shiftright', None, 'Shift_R')
    SLEEP = _IrisKey('sleep', None)
    STOP = _IrisKey('stop', None)
    SUBTRACT = _IrisKey('subtract', None, 'KP_Subtract')
    VOLUME_DOWN = _IrisKey('volumedown', None)
    VOLUME_MUTE = _IrisKey('volumemute', None)
    VOLUME_UP = _IrisKey('volumeup', None)
    WIN_LEFT = _IrisKey('winleft', None, 'Super_L')
    WIN_RIGHT = _IrisKey('winright', None, 'Super_R')
    YEN = _IrisKey('yen', None)

    @staticmethod
    def is_lock_on(keyboard_key: str):
        """Static method which determines if a keyboard key(CAPS LOCK, NUM LOCK or SCROLL LOCK) is ON.

        :param keyboard_key: Keyboard key(CAPS LOCK, NUM LOCK or SCROLL LOCK).
        :return: TRUE if keyboard_key state is ON or FALSE if keyboard_key state is OFF.
        """
        if Settings.get_os() == OSPlatform.WINDOWS:
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
        elif Settings.get_os() == OSPlatform.LINUX or Settings.get_os() == OSPlatform.MAC:
            try:
                cmd = subprocess.Popen('xset q', shell=True, stdout=subprocess.PIPE)
                shutdown_process('Xquartz')
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
    def get_active_modifiers(value: str):
        """Gets all the active modifiers depending on the used OS.

        :param value: Key modifier.
        :return: Returns an array with all the active modifiers.
        """
        all_modifiers = [
            Key.SHIFT,
            Key.CTRL]
        if Settings.get_os() == OSPlatform.MAC:
            all_modifiers.append(Key.CMD)
        elif Settings.get_os() == OSPlatform.WINDOWS:
            all_modifiers.append(Key.WIN)
        else:
            all_modifiers.append(Key.META)

        all_modifiers.append(Key.ALT)

        active_modifiers = []
        for item in all_modifiers:
            if item.value & value:
                active_modifiers.append(item.label)
        return active_modifiers


def key_down(key: str):
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
        raise ValueError('')


def key_up(key: str):
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
        raise ValueError('')


def type(text: str = None, modifier: str = None, interval: int = None):
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

    if Settings.type_delay != Settings.DEFAULT_TYPE_DELAY:
        Settings.type_delay = Settings.DEFAULT_TYPE_DELAY


def paste(text: str):
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

    if Settings.get_os() == OSPlatform.MAC:
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


@staticmethod
def shutdown_process(process_name: str):
    """Checks if the process name exists in the process list and close it .

    """

    if Settings.get_os() == OSPlatform.WINDOWS:
        command_str = 'taskkill /IM ' + process_name + '.exe'
        try:
            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception('Unable to run Command.')
    elif Settings.get_os() == OSPlatform.MAC or Settings.get_os() == OSPlatform.LINUX:
        command_str = 'pkill ' + process_name
        try:
            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception('Unable to run Command.')
