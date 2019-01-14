# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import subprocess
from datetime import time

import pyautogui
import pyperclip

from iris2.src.core.api.arg_parser import parse_args, logger
from iris2.src.core.api.enums import OSPlatform
from iris2.src.core.api.errors import FindError
from iris2.src.core.api.keyboard.key import KeyModifier, _IrisKey, Key
from iris2.src.core.api.settings import Settings

DEFAULT_KEY_SHORTCUT_DELAY = 0.1


def key_down(key: type):
    """Performs a keyboard key press without the release. This will put that key in a held down state.

    :param key: The key to be pressed down.
    :return: None.
    """
    if isinstance(key, _IrisKey):
        pyautogui.keyDown(key)
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyDown(key)
        else:
            raise ValueError("Unsupported string input.")
    else:
        raise ValueError('')


def key_up(key: type):
    """Performs a keyboard key release (without the press down beforehand).

    :param key: The key to be released up.
    :return: None.
    """
    if isinstance(key, _IrisKey):
        pyautogui.keyUp(key)
    elif isinstance(key, str):
        if pyautogui.isValidKey(key):
            pyautogui.keyUp(key)
        else:
            raise ValueError("Unsupported string input.")
    else:
        raise ValueError('')


def press_key(text: str = None, modifier: type = None, interval: int = None):
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
            key_down(str(text))
            key_up(str(text))
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
            key_down(modifier_keys[0])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_down(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_up(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_up(modifier_keys[0])
        elif num_keys == 2:
            key_down(modifier_keys[0])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_down(modifier_keys[1])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_down(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            key_up(str(text))
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

    if Settings.get_os() == OSPlatform.MAC:
        type(text='v', modifier=KeyModifier.CMD)
    else:
        type(text='v', modifier=KeyModifier.CTRL)

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
