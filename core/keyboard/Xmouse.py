# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from Xlib import X
from Xlib.ext.xtest import fake_input

from core.helpers.location import Location
from core.keyboard.Xkeyboard import XKeyboard


class XMouse(XKeyboard):

    def __init__(self):
        self.MOUSE_BUTTONS = {'left': 1, 'middle': 2, 'right': 3, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}

    def click(self, location: Location, button: str):
        assert button in self.MOUSE_BUTTONS.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
        button = self.MOUSE_BUTTONS[button]

        self._mouseDown(location, button)
        self._mouseUp(location, button)

    def _vertical_scroll(self, clicks: int, location: Location = None):
        clicks = int(clicks)
        if clicks == 0:
            return
        elif clicks > 0:
            button = 4  # scroll up
        else:
            button = 5  # scroll down

        for i in range(abs(clicks)):
            self.click(location, button=button)

    def _horizontal_scroll(self, clicks, location: Location):
        clicks = int(clicks)
        if clicks == 0:
            return
        elif clicks > 0:
            button = 7  # scroll right
        else:
            button = 6  # scroll left

        for i in range(abs(clicks)):
            self.click(location, button=button)

    def scroll(self, clicks, location: Location):
        return self.vertical_scroll(clicks, location)

    def _moveTo(self, location: Location):
        fake_input(self._display, X.MotionNotify, x=location.x, y=location.y)
        self._display.sync()

    def _mouseDown(self, location: Location, button):
        self._moveTo(location)
        assert button in self.MOUSE_BUTTONS.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
        button = self.MOUSE_BUTTONS[button]
        fake_input(self._display, X.ButtonPress, button)
        self._display.sync()

    def _mouseUp(self, location: Location, button):
        self._moveTo(location)
        assert button in self.MOUSE_BUTTONS.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
        button = self.MOUSE_BUTTONS[button]
        fake_input(self._display, X.ButtonRelease, button)
        self._display.sync()

    def position(self):
        """Returns:
          (x, y) tuple of the current xy coordinates of the mouse cursor.
        """
        coord = self.display.screen().root.query_pointer()._data
        position = (coord["root_x"], coord["root_y"])
        return position
