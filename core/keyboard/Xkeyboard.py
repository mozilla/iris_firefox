# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
import Xlib.XK


class XKeyboard:

    def __init__(self):
        """
        Initializing a X Display that will be used for screenshot , keyboard and mouse
        actions in a framebuffer environment

        """

        self.display = Display(os.environ['DISPLAY'])

    def _screen_size(self):
        """
        Performs a keyboard key press without the release. This will put that
            key in a held down state.

            Args:
            key (str): The key to be pressed down. The valid names are listed in
            Key class

            Returns:
                 Screen Width and Height
        """

        return self.display.screen().width_in_pixels, self.display.screen().height_in_pixels

    def keyDown(self, key):
        """
        Performs a keyboard key press without the release. This will put that
        key in a held down state.

        Args:
          key (str): The key to be pressed down. The valid names are listed in
          Key class

        Returns:
          None
        """
        if self.keyboardMapping(key) is None:
            return

        if type(key) == int:
            fake_input(self.display, X.KeyPress, key)
            self.display.sync()
            return

        needsShift = isShiftCharacter(key)
        if needsShift:
            fake_input(self.display, X.KeyPress, self.keyboardMapping('shift'))

        fake_input(self.display, X.KeyPress, self.keyboardMapping(key))

        if needsShift:
            fake_input(self.display, X.KeyRelease, self.keyboardMapping('shift'))
        self.display.sync()

    def keyUp(self, key):
        """
        Performs a keyboard key release (without the press down beforehand).

        Args:
          key (str): The key to be released up. The valid names are listed in
          Key Class

        Returns:
          None
        """

        if self.keyboardMapping(key) is None:
            return

        if type(key) == int:
            keycode = key
        else:
            keycode = self.keyboardMapping(key)

        fake_input(self.display, X.KeyRelease, keycode)
        self.display.sync()

    def keyboardMapping(self, iriskey: type):

        return self.display.keysym_to_keycode(Xlib.XK.string_to_keysym(iriskey))


@staticmethod
def isShiftCharacter(character):
    """
    Returns True if the key character is uppercase or shifted.
    """
    return character.isupper() or character in '~!@#$%^&*()_+{}|:"<>?'

