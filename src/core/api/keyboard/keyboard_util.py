# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import ctypes
import logging
import re
import subprocess

import pyautogui
import pyperclip

from src.core.api.keyboard.key import Key
from src.core.api.os_helpers import OSHelper
from src.core.util.arg_parser import logger
from src.core.util.system import shutdown_process

logger = logging.getLogger(__name__)
DEFAULT_KEY_SHORTCUT_DELAY = 0.1
pyautogui.FAILSAFE = False


def get_clipboard():
    """Return the content copied to clipboard."""
    return pyperclip.paste()


def is_lock_on(key):
    """Determines if a keyboard key(CAPS LOCK, NUM LOCK or SCROLL LOCK) is ON.

    :param key: Keyboard key(CAPS LOCK, NUM LOCK or SCROLL LOCK).
    :return: TRUE if keyboard_key state is ON or FALSE if keyboard_key state is OFF.
    """
    if OSHelper.is_windows():
        hll_dll = ctypes.WinDLL("User32.dll")
        keyboard_code = 0
        if key == Key.CAPS_LOCK:
            keyboard_code = 0x14
        elif key == Key.NUM_LOCK:
            keyboard_code = 0x90
        elif key == Key.SCROLL_LOCK:
            keyboard_code = 0x91
        try:
            key_state = hll_dll.GetKeyState(keyboard_code) & 1
        except Exception:
            raise Exception('Unable to run Command.')
        if key_state == 1:
            return True
        return False

    elif OSHelper.is_linux() or OSHelper.is_mac():
        try:
            cmd = subprocess.Popen('xset q', shell=True, stdout=subprocess.PIPE)
            shutdown_process('Xquartz')
        except subprocess.CalledProcessError as e:
            logger.error('Command  failed: %s' % repr(e.cmd))
            raise Exception('Unable to run Command.')
        else:
            processed_lock_key = key.value.label
            if 'caps' in processed_lock_key:
                processed_lock_key = 'Caps'
            elif 'num' in processed_lock_key:
                processed_lock_key = 'Num'
            elif 'scroll' in processed_lock_key:
                processed_lock_key = 'Scroll'

            for line in cmd.stdout:
                line = line.decode("utf-8")
                if processed_lock_key in line:
                    values = re.findall('\d*\D+', ' '.join(line.split()))
                    for val in values:
                        if processed_lock_key in val and 'off' in val:
                            return False
        return True


def check_keyboard_state(disable=False):
    """Check Keyboard state.

    Iris cannot run in case Key.CAPS_LOCK, Key.NUM_LOCK or Key.SCROLL_LOCK are pressed.
    """
    if disable:
        return True

    key_on = False
    keyboard_keys = [Key.CAPS_LOCK, Key.NUM_LOCK, Key.SCROLL_LOCK]
    for key in keyboard_keys:
        if is_lock_on(key):
            logger.error('Cannot run Iris because %s is on. Please turn it off to continue.' % key.value.label.upper())
            key_on = True
    return not key_on


def get_active_modifiers(key):
    """Gets all the active modifiers depending on the used OS.

    :param key: Key modifier.
    :return: Returns an array with all the active modifiers.
    """
    all_modifiers = [
        Key.SHIFT,
        Key.CTRL]
    if OSHelper.is_mac():
        all_modifiers.append(Key.CMD)
    elif OSHelper.is_windows():
        all_modifiers.append(Key.WIN)
    else:
        all_modifiers.append(Key.META)

    all_modifiers.append(Key.ALT)

    active_modifiers = []
    for item in all_modifiers:
        try:
            for key_value in key:

                if item == key_value.value:
                    active_modifiers.append(item)
        except TypeError:
            if item == key.value:
                active_modifiers.append(item)

    return active_modifiers


def is_shift_character(character):
    """
    Returns True if the key character is uppercase or shifted.
    """
    return character.isupper() or character in '~!@#$%^&*()_+{}|:"<>?'
