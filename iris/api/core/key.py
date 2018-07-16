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
from util.core_helper import INVALID_GENERIC_INPUT

DEFAULT_KEY_SHORTCUT_DELAY = 0.1

logger = logging.getLogger(__name__)


class IrisKey(object):
    def __init__(self, label, value=None, reserved=True):
        self.label = label
        self.value = value
        self.is_reserved = reserved

    def __str__(self):
        return self.label


class Key(object):
    ADD = IrisKey('add')
    ALT = IrisKey('alt', 1 << 3)
    BACKSPACE = IrisKey('backspace')
    CAPS_LOCK = IrisKey('capslock')
    CMD = IrisKey('command', 1 << 2)
    CTRL = IrisKey('ctrl', 1 << 1)
    DELETE = IrisKey('del')
    DIVIDE = IrisKey('divide')
    DOWN = IrisKey('down')
    ENTER = '\n'
    END = IrisKey('end')
    ESC = IrisKey('esc')
    F1 = IrisKey('f1')
    F2 = IrisKey('f2')
    F3 = IrisKey('f3')
    F4 = IrisKey('f4')
    F5 = IrisKey('f5')
    F6 = IrisKey('f6')
    F7 = IrisKey('f7')
    F8 = IrisKey('f8')
    F9 = IrisKey('f9')
    F10 = IrisKey('f10')
    F11 = IrisKey('f11')
    F12 = IrisKey('f12')
    F13 = IrisKey('f13')
    F14 = IrisKey('f14')
    F15 = IrisKey('f15')
    HOME = IrisKey('home')
    INSERT = IrisKey('insert')
    LEFT = IrisKey('left')
    META = IrisKey('winleft', 1 << 2)
    MINUS = IrisKey('subtract')
    MULTIPLY = IrisKey('multiply')
    NUM0 = IrisKey('num0')
    NUM1 = IrisKey('num1')
    NUM2 = IrisKey('num2')
    NUM3 = IrisKey('num3')
    NUM4 = IrisKey('num4')
    NUM5 = IrisKey('num5')
    NUM6 = IrisKey('num6')
    NUM7 = IrisKey('num7')
    NUM8 = IrisKey('num8')
    NUM9 = IrisKey('num9')
    NUM_LOCK = IrisKey('numlock')
    PAGE_DOWN = IrisKey('pagedown')
    PAGE_UP = IrisKey('pageup')
    PAUSE = IrisKey('pause')
    PRINT_SCREEN = IrisKey('printscreen')
    RIGHT = IrisKey('right')
    SCROLL_LOCK = IrisKey('scrolllock')
    SEPARATOR = IrisKey('separator')
    SHIFT = IrisKey('shift', 1 << 0)
    SPACE = ' '
    TAB = '\t'
    UP = IrisKey('up')
    WIN = IrisKey('win', 1 << 2)

    # Additional keys
    ACCEPT = IrisKey('accept')
    ALT_LEFT = IrisKey('altleft')
    ALT_RIGHT = IrisKey('altright')
    APPS = IrisKey('apps')
    BROWSER_BACK = IrisKey('browserback')
    BROWSER_FAVORITES = IrisKey('browserfavorites')
    BROWSER_FORWARD = IrisKey('browserforward')
    BROWSER_HOME = IrisKey('browserhome')
    BROWSER_REFRESH = IrisKey('browserrefresh')
    BROWSER_SEARCH = IrisKey('browsersearch')
    BROWSER_STOP = IrisKey('browserstop')
    CLEAR = IrisKey('clear')
    COMMAND = IrisKey('command')
    CONVERT = IrisKey('convert')
    CTRL_LEFT = IrisKey('ctrlleft')
    CTRL_RIGHT = IrisKey('ctrlright')
    DECIMAL = IrisKey('decimal')
    EXECUTE = IrisKey('execute')
    F16 = IrisKey('f16')
    F17 = IrisKey('f17')
    F18 = IrisKey('f18')
    F19 = IrisKey('f19')
    F20 = IrisKey('f20')
    F21 = IrisKey('f21')
    F22 = IrisKey('f22')
    F23 = IrisKey('f23')
    F24 = IrisKey('f24')
    FINAL = IrisKey('final')
    FN = IrisKey('fn')
    HANGUEL = IrisKey('hanguel')
    HANGUL = IrisKey('hangul')
    HANJA = IrisKey('hanja')
    HELP = IrisKey('help')
    JUNJA = IrisKey('junja')
    KANA = IrisKey('kana')
    KANJI = IrisKey('kanji')
    LAUNCH_APP1 = IrisKey('launchapp1')
    LAUNCH_APP2 = IrisKey('launchapp2')
    LAUNCH_MAIL = IrisKey('launchmail')
    LAUNCH_MEDIA_SELECT = IrisKey('launchmediaselect')
    MODE_CHANGE = IrisKey('modechange')
    NEXT_TRACK = IrisKey('nexttrack')
    NONCONVERT = IrisKey('nonconvert')
    OPTION = IrisKey('option')
    OPTION_LEFT = IrisKey('optionleft')
    OPTION_RIGHT = IrisKey('optionright')
    PGDN = IrisKey('pgdn')
    PGUP = IrisKey('pgup')
    PLAY_PAUSE = IrisKey('playpause')
    PREV_TRACK = IrisKey('prevtrack')
    PRINT = IrisKey('print')
    PRNT_SCRN = IrisKey('prntscrn')
    PRTSC = IrisKey('prtsc')
    PRTSCR = IrisKey('prtscr')
    RETURN = IrisKey('return')
    SELECT = IrisKey('select')
    SHIFT_LEFT = IrisKey('shiftleft')
    SHIFT_RIGHT = IrisKey('shiftright')
    SLEEP = IrisKey('sleep')
    STOP = IrisKey('stop')
    SUBTRACT = IrisKey('subtract')
    VOLUME_DOWN = IrisKey('volumedown')
    VOLUME_MUTE = IrisKey('volumemute')
    VOLUME_UP = IrisKey('volumeup')
    WIN_LEFT = IrisKey('winleft')
    WIN_RIGHT = IrisKey('winright')
    YEN = IrisKey('yen')

    @staticmethod
    def is_lock_on(keyboard_key):
        if Settings.get_os() == Platform.WINDOWS:
            keyboard_code = 0
            hll_dll = ctypes.WinDLL("User32.dll")
            if keyboard_key == Key.CAPS_LOCK:
                keyboard_code = 0x14
            elif keyboard_key == Key.NUM_LOCK:
                keyboard_code = 0x90
            elif keyboard_key == Key.SCROLL_LOCK:
                keyboard_code = 0x91
            try:
                key_state = hll_dll.GetKeyState(keyboard_code)
            except Exception:
                raise Exception('Unable to run Command')
            if key_state == 1:
                return True
            else:
                return False
        elif Settings.get_os() == Platform.LINUX or Settings.get_os() == Platform.MAC:
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
                if Settings.get_os() == Platform.MAC:
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


def shutdown_process(process_name):
    if Settings.get_os() == Platform.WINDOWS:
        command_str = 'taskkill /IM ' + process_name + '.exe'
        try:

            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception('Unable to run Command')
    elif Settings.get_os() == Platform.MAC or Settings.get_os() == Platform.LINUX:
        command_str = 'pkill ' + process_name
        try:
            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception('Unable to run Command')


def key_down(key):
    if isinstance(key, IrisKey):
        pyautogui.keyDown(str(key))
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyDown(key)
        else:
            raise ValueError("Unsupported string input")
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def key_up(key):
    if isinstance(key, IrisKey):
        pyautogui.keyUp(str(key))
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyUp(key)
        else:
            raise ValueError("Unsupported string input")
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def type(text=None, modifier=None, interval=None):
    logger.debug('type method: ')
    if modifier is None:
        if isinstance(text, IrisKey):
            logger.debug('Scenario 1: reserved key')
            logger.debug('Reserved key: %s' % text)
            pyautogui.keyDown(str(text))
            pyautogui.keyUp(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
        else:
            if interval is None:
                interval = Settings.type_delay

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

    if Settings.type_delay != DEFAULT_TYPE_DELAY:
        Settings.type_delay = DEFAULT_TYPE_DELAY


def paste(text):
    # load to clipboard
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
        logger.error('Paste method failed')
        raise FindError

    if Settings.get_os() == Platform.MAC:
        type(text='v', modifier=KeyModifier.CMD)
    else:
        type(text='v', modifier=KeyModifier.CTRL)
    # clear clipboard
    pyperclip.copy('')
