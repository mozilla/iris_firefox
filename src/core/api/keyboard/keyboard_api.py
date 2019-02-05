# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import ctypes
import re
import subprocess
import time
from typing import List

import pyautogui
import pyperclip

from src.core.api.arg_parser import logger
from src.core.api.errors import FindError
from src.core.api.keyboard.key import KeyModifier, Key
from src.core.api.os_helpers import OSHelper
from src.core.api.settings import Settings
from src.core.util.system import shutdown_process

DEFAULT_KEY_SHORTCUT_DELAY = 0.1


def key_down(key):
    """Performs a keyboard key press without the release. This will put that key in a held down state.

    :param key: The key to be pressed down.
    :return: None.
    """
    if isinstance(key, Key):
        pyautogui.keyDown(key.value.label)
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyDown(key)
        else:
            raise ValueError("Unsupported Key input.")
    else:
        raise ValueError("Unsupported Key input.")


def key_up(key):
    """Performs a keyboard key release (without the press down beforehand).

    :param key: The key to be released up.
    :return: None.
    """
    if isinstance(key, Key):
        pyautogui.keyUp(key.value.label)
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyUp(key)
        else:
            raise ValueError("Unsupported Key input.")
    else:
        raise ValueError("Unsupported Key input.")


def type(text: Key or str = None, modifier: Key or List[Key] = None, interval: int = None):
    """
    :param str || list text: If a string, then the characters to be pressed. If a list, then the key names of the keys
                             to press in order.
    :param modifier: Key modifier.
    :param interval: The number of seconds in between each press. By default it is 0 seconds.
    :return: None.
    """
    logger.debug('type method: ')
    if modifier is None:
        if isinstance(text, Key):
            logger.debug('Scenario 1: reserved key.')
            logger.debug('Reserved key: %s' % text)
            key_down(text)
            key_up(text)
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
        else:
            if interval is None:
                interval = Settings.type_delay

            logger.debug('Scenario 2: normal key or text block.')
            logger.debug('Text: %s' % text)
            pyautogui.typewrite(text, interval)
    else:
        logger.debug('Scenario 3: combination of modifiers and other keys.')
        modifier_keys = get_active_modifiers(modifier)
        num_keys = len(modifier_keys)
        logger.debug('Modifiers (%s): %s ' % (num_keys, ' '.join(key.name for key in modifier_keys)))
        logger.debug('text: %s' % text)
        if num_keys == 1:
            key_down(modifier_keys[0])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_down(text)
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_up(text)
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_up(modifier_keys[0])
        elif num_keys == 2:
            key_down(modifier_keys[0])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_down(modifier_keys[1])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_down(text)
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_up(text)
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_up(modifier_keys[1])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_up(modifier_keys[0])
        else:
            logger.error('Returned key modifiers out of range.')

    if Settings.type_delay != Settings.DEFAULT_TYPE_DELAY:
        Settings.type_delay = Settings.DEFAULT_TYPE_DELAY


def paste(text: str):
    """
    :param text: Text to be pasted.
    :return: None.
    """

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

    if OSHelper.is_mac():
        type(text='v', modifier=KeyModifier.CMD)
    else:
        type(text='v', modifier=KeyModifier.CTRL)

    pyperclip.copy('')


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
