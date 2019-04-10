# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
from enum import Enum

logger = logging.getLogger(__name__)


class KeyCode:
    def __init__(self, label: str, value=None, x11key: str = None, reserved: bool = True):
        self.label = label
        self.value = value
        self.x11key = x11key
        self.is_reserved = reserved

    def __str__(self):
        return self.label


class Key(Enum):
    """Class with multiple instances of the KeyCode class."""

    ADD = KeyCode('add', None, 'KP_Add')
    ALT = KeyCode('alt', 1 << 3, 'Alt_L')
    BACKSPACE = KeyCode('backspace', None, 'BackSpace')
    CAPS_LOCK = KeyCode('capslock', None, 'Caps_Lock')
    CMD = KeyCode('command', 1 << 2, 'Command')
    CTRL = KeyCode('ctrl', 1 << 1, 'Control_L')
    DELETE = KeyCode('del', None, 'Delete')
    DIVIDE = KeyCode('divide', None, 'KP_Divide')
    DOWN = KeyCode('down', None, 'Down')
    ENTER = KeyCode('\n', None, 'Return')
    END = KeyCode('end', None, 'End')
    ESC = KeyCode('esc', None, 'Escape')
    F1 = KeyCode('f1', None, 'F1')
    F2 = KeyCode('f2', None, 'F2')
    F3 = KeyCode('f3', None, 'F3')
    F4 = KeyCode('f4', None, 'F4')
    F5 = KeyCode('f5', None, 'F5')
    F6 = KeyCode('f6', None, 'F6')
    F7 = KeyCode('f7', None, 'F7')
    F8 = KeyCode('f8', None, 'F8')
    F9 = KeyCode('f9', None, 'F9')
    F10 = KeyCode('f10', None, 'F10')
    F11 = KeyCode('f11', None, 'F11')
    F12 = KeyCode('f12', None, 'F12')
    F13 = KeyCode('f13', None, 'F13')
    F14 = KeyCode('f14', None, 'F14')
    F15 = KeyCode('f15', None, 'F15')
    HOME = KeyCode('home', None, 'Home')
    INSERT = KeyCode('insert', None, 'Insert')
    LEFT = KeyCode('left', None, 'Left')
    META = KeyCode('winleft', 1 << 2, 'Super_L')
    MINUS = KeyCode('subtract', None)
    MULTIPLY = KeyCode('multiply', None, 'KP_Multiply')
    NUM0 = KeyCode('num0', None, 'KP_0')
    NUM1 = KeyCode('num1', None, 'KP_1')
    NUM2 = KeyCode('num2', None, 'KP_2')
    NUM3 = KeyCode('num3', None, 'KP_3')
    NUM4 = KeyCode('num4', None, 'KP_4')
    NUM5 = KeyCode('num5', None, 'KP_5')
    NUM6 = KeyCode('num6', None, 'KP_6')
    NUM7 = KeyCode('num7', None, 'KP_7')
    NUM8 = KeyCode('num8', None, 'KP_8')
    NUM9 = KeyCode('num9', None, 'KP_9')
    NUM_LOCK = KeyCode('numlock', None, 'Num_Lock')
    PAGE_DOWN = KeyCode('pagedown', None, 'Page_Down')
    PAGE_UP = KeyCode('pageup', None, 'Page_Up')
    PAUSE = KeyCode('pause', None, 'Pause')
    PRINT_SCREEN = KeyCode('printscreen', None, 'Print')
    RIGHT = KeyCode('right', None, 'Right')
    SCROLL_LOCK = KeyCode('scrolllock', None, 'Scroll_Lock')
    SEPARATOR = KeyCode('separator', None, 'KP_Separator')
    SHIFT = KeyCode('shift', 1 << 0, 'Shift_L')
    SPACE = KeyCode(' ', None, 'space')
    TAB = KeyCode('\t', None, 'Tab')
    UP = KeyCode('up', None, 'Up')
    WIN = KeyCode('win', 1 << 2)

    ACCEPT = KeyCode('accept', None)
    ALT_LEFT = KeyCode('altleft', None, 'Alt_L')
    ALT_RIGHT = KeyCode('altright', None, 'Alt_R')
    APPS = KeyCode('apps', None, 'Super_L')
    BROWSER_BACK = KeyCode('browserback', None)
    BROWSER_FAVORITES = KeyCode('browserfavorites', None)
    BROWSER_FORWARD = KeyCode('browserforward', None)
    BROWSER_HOME = KeyCode('browserhome', None)
    BROWSER_REFRESH = KeyCode('browserrefresh', None)
    BROWSER_SEARCH = KeyCode('browsersearch', None)
    BROWSER_STOP = KeyCode('browserstop', None)
    CLEAR = KeyCode('clear', None)
    COMMAND = KeyCode('command', None)
    CONVERT = KeyCode('convert', None)
    CTRL_LEFT = KeyCode('ctrlleft', None, 'Control_L')
    CTRL_RIGHT = KeyCode('ctrlright', None, 'Control_R')
    DECIMAL = KeyCode('decimal', None, 'KP_Decimal')
    EXECUTE = KeyCode('execute', None, 'Execute')
    F16 = KeyCode('f16', None, 'F16')
    F17 = KeyCode('f17', None, 'F17')
    F18 = KeyCode('f18', None, 'F18')
    F19 = KeyCode('f19', None, 'F19')
    F20 = KeyCode('f20', None, 'F20')
    F21 = KeyCode('f21', None, 'F21')
    F22 = KeyCode('f22', None, 'F22')
    F23 = KeyCode('f23', None, 'F23')
    F24 = KeyCode('f24', None, 'F24')
    FINAL = KeyCode('final', None)
    FN = KeyCode('fn', None)
    HANGUEL = KeyCode('hanguel', None)
    HANGUL = KeyCode('hangul', None)
    HANJA = KeyCode('hanja', None)
    HELP = KeyCode('help', None, 'Help')
    JUNJA = KeyCode('junja', None)
    KANA = KeyCode('kana', None)
    KANJI = KeyCode('kanji', None)
    LAUNCH_APP1 = KeyCode('launchapp1', None)
    LAUNCH_APP2 = KeyCode('launchapp2', None)
    LAUNCH_MAIL = KeyCode('launchmail', None)
    LAUNCH_MEDIA_SELECT = KeyCode('launchmediaselect', None)
    MODE_CHANGE = KeyCode('modechange', None)
    NEXT_TRACK = KeyCode('nexttrack', None)
    NONCONVERT = KeyCode('nonconvert', None)
    OPTION = KeyCode('option', None)
    OPTION_LEFT = KeyCode('optionleft', None)
    OPTION_RIGHT = KeyCode('optionright', None)
    PGDN = KeyCode('pgdn', None)
    PGUP = KeyCode('pgup', None)
    PLAY_PAUSE = KeyCode('playpause', None)
    PREV_TRACK = KeyCode('prevtrack', None)
    PRINT = KeyCode('print', None, 'Print')
    PRNT_SCRN = KeyCode('prntscrn', None, 'Print')
    PRTSC = KeyCode('prtsc', None)
    PRTSCR = KeyCode('prtscr', None)
    RETURN = KeyCode('return', None)
    SELECT = KeyCode('select', None, 'Select')
    SHIFT_LEFT = KeyCode('shiftleft', None, 'Shift_L')
    SHIFT_RIGHT = KeyCode('shiftright', None, 'Shift_R')
    SLEEP = KeyCode('sleep', None)
    STOP = KeyCode('stop', None)
    SUBTRACT = KeyCode('subtract', None, 'KP_Subtract')
    VOLUME_DOWN = KeyCode('volumedown', None)
    VOLUME_MUTE = KeyCode('volumemute', None)
    VOLUME_UP = KeyCode('volumeup', None)
    WIN_LEFT = KeyCode('winleft', None, 'Super_L')
    WIN_RIGHT = KeyCode('winright', None, 'Super_R')
    YEN = KeyCode('yen', None)


class KeyModifier(Enum):
    """Keyboard key variables."""
    SHIFT = Key.SHIFT
    CTRL = Key.CTRL
    CMD = Key.CMD
    WIN = Key.WIN
    META = Key.META
    ALT = Key.ALT
