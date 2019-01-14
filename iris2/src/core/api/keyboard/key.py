# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import ctypes
import logging
import subprocess

from iris2.src.core.api.enums import OSPlatform
from iris2.src.core.api.keyboard.keyboard_api import shutdown_process
from iris2.src.core.api.settings import Settings
from iris2.src.core.util.os_helpers import OSHelper

logger = logging.getLogger(__name__)


class _IrisKey(object):

    def __init__(self, label: str, value: type = None, x11key: str = None, reserved: type = True):
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
    def is_lock_on(keyboard_key: type):
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
        if OSHelper.get_os() == OSPlatform.MAC:
            all_modifiers.append(Key.CMD)
        elif OSHelper.get_os() == OSPlatform.WINDOWS:
            all_modifiers.append(Key.WIN)
        else:
            all_modifiers.append(Key.META)

        all_modifiers.append(Key.ALT)

        active_modifiers = []
        for item in all_modifiers:
            if item.value & value:
                active_modifiers.append(item.label)
        return active_modifiers
