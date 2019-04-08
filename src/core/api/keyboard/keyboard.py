# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pyautogui

from src.core.util.arg_parser import get_core_args
import logging
import os
import time

from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
import Xlib.XK
from src.core.api.keyboard.key import Key, KeyModifier
from src.core.api.keyboard.keyboard_util import get_active_modifiers, is_shift_character
from src.core.api.settings import Settings

logger = logging.getLogger(__name__)
DEFAULT_KEY_SHORTCUT_DELAY = 0.1
pyautogui.FAILSAFE = False

use_virtual_keyboard = get_core_args().virtual_keyboard


def key_down(key):
    """Performs a keyboard key press without the release. This will put that key in a held down state.

    :param key: The key to be pressed down.
    :return: None.
    """
    if use_virtual_keyboard:
        virtual_keyboard.key_down(key)
    else:
        _Keyboard.key_down(key)


def key_up(key):
    """Performs a keyboard key release (without the press down beforehand).

    :param key: The key to be released up.
    :return: None.
    """
    if use_virtual_keyboard:
        virtual_keyboard.key_up(key)
    else:
        _Keyboard.key_up(key)


def type(text: Key or str = None, modifier=None, interval: int = None):
    """
    :param str || list text: If a string, then the characters to be pressed. If a list, then the key names of the keys
                             to press in order.
    :param modifier: Key modifier.
    :param interval: The number of seconds in between each press. By default it is 0 seconds.
    :return: None.
    """
    if use_virtual_keyboard:
        _XKeyboard.type(text, modifier, interval)
    else:
        _Keyboard.type(text, modifier, interval)


class XScreen:

    def _screen_size(self):
        """
            Returns:
                 Screen Width and Height of the virtual screen
        """

        return self.display.screen().width_in_pixels, self.display.screen().height_in_pixels


class _XKeyboard(XScreen):

    def __init__(self):

        self.display = Display(os.environ['DISPLAY'])

    def key_down(self, key):
        """
        Performs a keyboard key press without the release. This will put that
        key in a held down state.

        Args:
          key (str): The key to be pressed down. The valid names are listed in
          Key class

        Returns:
          None
        """

        if isinstance(key, Key) or isinstance(key, KeyModifier):
            key = key.value.x11key

        if self.keyboard_mapping(key) is None:
            return

        if isinstance(key, int):
            fake_input(self.display, X.KeyPress, key)
            self.display.sync()
            return

        needs_shift = is_shift_character(key)
        if needs_shift:
            fake_input(self.display, X.KeyPress, self.keyboard_mapping('shift'))

        fake_input(self.display, X.KeyPress, self.keyboard_mapping(key))

        if needs_shift:
            fake_input(self.display, X.KeyRelease, self.keyboard_mapping('shift'))
        self.display.sync()

    def press(self, characters, interval):
        """
        Performs a keyboard key press down, followed by a release

        Args:
          key (str): The key to be released up. The valid names are listed in
          Key Class

        Returns:
          None
        """

        if type(characters) == str:
            characters = [characters]  # put string in a list
        else:
            lower_keys = []
            for s in characters:
                if len(s) > 1:
                    lower_keys.append(s.lower())
                else:
                    lower_keys.append(s)
        interval = float(interval)
        for k in characters:
            self.key_down(k)
            self.key_up(k)
            time.sleep(interval)

    def key_up(self, key):
        """
        Performs a keyboard key release (without the press down beforehand).

        Args:
          key (str): The key to be released up. The valid names are listed in
          Key Class

        Returns:
          None
        """

        if isinstance(key, Key) or isinstance(key, KeyModifier):
            key = key.value.x11key

        if self.keyboard_mapping(key) is None:
            return

        if isinstance(key, int):
            keycode = key
        else:
            keycode = self.keyboard_mapping(key)

        fake_input(self.display, X.KeyRelease, keycode)
        self.display.sync()

    def type_write(self, keys, interval: int = None):
        """
       "Performs a keyboard key press down, followed by a release, for each of the characters in message.

        Args:
          :param  str || list  keys: The message argument can also be list of strings, in which case any valid
                      keyboard name can be used.
          :param interval: The number of seconds in between each press. By default it is 0 seconds.

        Returns:
          None
        """

        for character in keys:
            if len(character) > 1:
                c = c.lower()
            self.press(c, interval)
            time.sleep(interval)

    def keyboard_mapping(self, iriskey):

        return self.display.keysym_to_keycode(Xlib.XK.string_to_keysym(iriskey))

    @staticmethod
    def type(text: Key or str = None, modifier=None, interval: int = None):
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
                virtual_keyboard.key_down(text)
                virtual_keyboard.key_up(text)
                time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            else:
                if interval is None:
                    interval = Settings.type_delay

                logger.debug('Scenario 2: normal key or text block.')
                logger.debug('text :')
                logger.debug(text)
                virtual_keyboard.type_write(text, interval)
        else:
            logger.debug('Scenario 3: combination of modifiers and other keys.')
            modifier_keys = get_active_modifiers(modifier)
            num_keys = len(modifier_keys)
            logger.debug('Modifiers (%s): %s ' % (num_keys, ' '.join(key.name for key in modifier_keys)))
            logger.debug('text: %s' % text)

            if num_keys == 1:
                virtual_keyboard.key_down(modifier_keys[0])
                time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
                virtual_keyboard.key_down(text)
                time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
                virtual_keyboard.key_up(text)
                time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
                virtual_keyboard.key_up(modifier_keys[0])
            elif num_keys == 2:
                virtual_keyboard.key_down(modifier_keys[0])
                time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
                virtual_keyboard.key_down(modifier_keys[1])
                time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
                virtual_keyboard.key_down(text)
                time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
                virtual_keyboard.key_up(text)
                time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
                virtual_keyboard.key_up(modifier_keys[1])
                time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
                virtual_keyboard.key_up(modifier_keys[0])
            else:
                logger.error('Returned key modifiers out of range.')

        if Settings.type_delay != Settings.DEFAULT_TYPE_DELAY:
            Settings.type_delay = Settings.DEFAULT_TYPE_DELAY

        logger.debug('END virtual type')


# Initialize fake keyboard

virtual_keyboard = _XKeyboard()


class _Keyboard(object):
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def type(text: Key or str = None, modifier=None, interval: int = None):
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
            from src.core.api.keyboard.keyboard_util import get_active_modifiers
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
