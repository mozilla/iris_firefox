# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
import time

import pyautogui

from src.core.api.keyboard.key import Key, KeyModifier
from src.core.api.keyboard.keyboard_util import get_active_modifiers, is_shift_character
from src.core.api.os_helpers import OSHelper
from src.core.api.settings import Settings
from src.core.util.arg_parser import get_core_args


logger = logging.getLogger(__name__)

try:
    from Xlib.display import Display
    from Xlib import X
    from Xlib.ext.xtest import fake_input
    import Xlib.XK
except ImportError:
    if OSHelper.is_linux():
        logger.error('Could not import Xlib modules.')
        exit(1)

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
    """Keyboard type.

    :param text: String or Key pressed
    :param modifier: Key modifier.
    :param interval: The number of seconds in between each press. By default it is 0 seconds.
    :return: None.
    """
    if use_virtual_keyboard:
        _XKeyboard.type(text, modifier, interval)
    else:
        _Keyboard.type(text, modifier, interval)


class XScreen:
    def __init__(self):
        self.display = Display(os.environ['DISPLAY'])

    def _screen_size(self):
        """Returns Screen Width and Height of the virtual screen. """
        return self.display.screen().width_in_pixels, self.display.screen().height_in_pixels


class _XKeyboard(XScreen):
    def key_down(self, key):
        """Performs a keyboard key press without the release. This will put that key in a held down state.

        :param key: The key to be pressed down. The valid names are listed in Key class
        :return: None.
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
        """Performs a keyboard key press down, followed by a release

        :param characters: The key to be released up. The valid names are listed in Key Class
        :param interval: Time between key presses
        :return: None.
        """
        if isinstance(characters, str):
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
        """Performs a keyboard key release (without the press down beforehand).

        :param key: The key to be released up. The valid names are listed in Key Class
        :return: None.
        """
        if isinstance(key, Key) or isinstance(key, KeyModifier):
            key = key.value.x11key

        if self.keyboard_mapping(key) is None:
            return

        if isinstance(key, int):
            key_code = key
        else:
            key_code = self.keyboard_mapping(key)

        fake_input(self.display, X.KeyRelease, key_code)
        self.display.sync()

    def type_write(self, keys, interval: int = None):
        """Performs a keyboard key press down, followed by a release, for each of the characters in message.

        :param keys: Can also be list of strings, in which case any valid keyboard name can be used.
        :param interval: The number of seconds in between each press. By default it is 0 seconds.
        :return: None.
        """
        for character in keys:
            if len(character) > 1:
                character = character.lower()
            self.press(character, interval)
            time.sleep(interval)

    def keyboard_mapping(self, key):
        return self.display.keysym_to_keycode(Xlib.XK.string_to_keysym(key))

    @staticmethod
    def type(text: Key or str = None, modifier=None, interval: int = None):
        """Keyboard type.

        :param text: String or Key pressed
        :param modifier: Key modifier.
        :param interval: The number of seconds in between each press. By default it is 0 seconds.
        :return: None.
        """
        if modifier is None:
            if isinstance(text, Key):
                logger.debug('Type Method: [Reserved key: {}]'.format(text))
                virtual_keyboard.key_down(text)
                virtual_keyboard.key_up(text)
                time.sleep(Settings.key_shortcut_delay)
            else:
                if interval is None:
                    interval = Settings.type_delay
                logger.debug('Type Method: [Text: {}]'.format(text))
                virtual_keyboard.type_write(text, interval)
        else:
            modifier_keys = get_active_modifiers(modifier)
            num_keys = len(modifier_keys)
            logger.debug('Type Method: [Modifiers ({}): {}] + [Text: {}]'
                         .format(num_keys, ' '.join(key.name for key in modifier_keys), text))

            if num_keys == 1:
                virtual_keyboard.key_down(modifier_keys[0])
                time.sleep(Settings.key_shortcut_delay)
                virtual_keyboard.key_down(text)
                time.sleep(Settings.key_shortcut_delay)
                virtual_keyboard.key_up(text)
                time.sleep(Settings.key_shortcut_delay)
                virtual_keyboard.key_up(modifier_keys[0])
            elif num_keys == 2:
                virtual_keyboard.key_down(modifier_keys[0])
                time.sleep(Settings.key_shortcut_delay)
                virtual_keyboard.key_down(modifier_keys[1])
                time.sleep(Settings.key_shortcut_delay)
                virtual_keyboard.key_down(text)
                time.sleep(Settings.key_shortcut_delay)
                virtual_keyboard.key_up(text)
                time.sleep(Settings.key_shortcut_delay)
                virtual_keyboard.key_up(modifier_keys[1])
                time.sleep(Settings.key_shortcut_delay)
                virtual_keyboard.key_up(modifier_keys[0])
            else:
                logger.error('Returned key modifiers out of range.')

        if Settings.type_delay != Settings.DEFAULT_TYPE_DELAY:
            Settings.type_delay = Settings.DEFAULT_TYPE_DELAY

        logger.debug('END virtual type')


if OSHelper.is_linux():
    virtual_keyboard = _XKeyboard()


class _Keyboard:
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
        """Keyboard type.

        :param text: String or Key pressed
        :param modifier: Key modifier.
        :param interval: The number of seconds in between each press. By default it is 0 seconds.
        :return: None.
        """
        if modifier is None:
            if isinstance(text, Key):
                logger.debug('Type Method: [Reserved key: {}]'.format(text))
                key_down(text)
                key_up(text)
                time.sleep(Settings.key_shortcut_delay)
            else:
                if interval is None:
                    interval = Settings.type_delay

                logger.debug('Type Method: [Text: {}]'.format(text))
                pyautogui.typewrite(text, interval)
        else:
            from src.core.api.keyboard.keyboard_util import get_active_modifiers
            modifier_keys = get_active_modifiers(modifier)
            num_keys = len(modifier_keys)
            logger.debug('Type Method: [Modifiers ({}): {}] + [Text: {}]'
                         .format(num_keys, ' '.join(key.name for key in modifier_keys), text))
            if num_keys == 1:
                key_down(modifier_keys[0])
                time.sleep(Settings.key_shortcut_delay)
                key_down(text)
                time.sleep(Settings.key_shortcut_delay)
                key_up(text)
                time.sleep(Settings.key_shortcut_delay)
                key_up(modifier_keys[0])
            elif num_keys == 2:
                key_down(modifier_keys[0])
                time.sleep(Settings.key_shortcut_delay)
                key_down(modifier_keys[1])
                time.sleep(Settings.key_shortcut_delay)
                key_down(text)
                time.sleep(Settings.key_shortcut_delay)
                key_up(text)
                time.sleep(Settings.key_shortcut_delay)
                key_up(modifier_keys[1])
                time.sleep(Settings.key_shortcut_delay)
                key_up(modifier_keys[0])
            else:
                logger.error('Returned key modifiers out of range.')

        if Settings.type_delay != Settings.DEFAULT_TYPE_DELAY:
            Settings.type_delay = Settings.DEFAULT_TYPE_DELAY
