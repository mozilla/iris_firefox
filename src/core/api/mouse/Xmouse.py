# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from Xlib import X
from Xlib.ext.xtest import fake_input

from core.helpers.location import Location
from core.keyboard.Xkeyboard import Xscreen


class XMouse(Xscreen):

    def __init__(self):
        self.display = Xscreen()
        self.MOUSE_BUTTONS = {'left': 1, 'middle': 2, 'right': 3, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}

    def click(self, location: Location, button: str):

        """
        Performs a click

        :param button :'left','middle','right'
        :param location :x,y coordinates where to click

        """

        assert button in self.MOUSE_BUTTONS.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
        button = self.MOUSE_BUTTONS[button]

        self._mouseDown(location, button)
        self._mouseUp(location, button)

    def _vertical_scroll(self, clicks: int, location: Location = None):

        """
        Performs a vertical mouse movement

        :param clicks :number of clicks
        :param location :x,y coordinates where to click

        """
        clicks = int(clicks)
        if clicks == 0:
            return
        elif clicks > 0:
            button = 4  # scroll up
        else:
            button = 5  # scroll down

        for i in range(abs(clicks)):
            self.click(location, button=button)

    def horizontal_scroll(self, clicks: int, location: Location):
        """
        Performs a horizontal mouse movement

        :param clicks :number of clicks
        :param location :x,y coordinates where to click

        """
        clicks = int(clicks)
        if clicks == 0:
            return
        elif clicks > 0:
            button = 7  # scroll right
        else:
            button = 6  # scroll left

        for i in range(abs(clicks)):
            self.click(location, button=button)

    def scroll(self, clicks: int, location: Location):
        """
        Performs a scroll mouse movement

        :param clicks :number of clicks
        :param location :x,y coordinates where to click

        """
        return self.vertical_scroll(clicks, location)

    def moveTo(self, location: Location):

        """
        Mouse move to specific Location

        :param location :x,y coordinates where to click

        """
        fake_input(self.display, X.MotionNotify, x=location.x, y=location.y)
        self.display.sync()

    def _mouseDown(self, location: Location, button: str):
        """
        Mouse button press

        :param location :x,y coordinates where to click
        :param button 'left','middle','right'

        """
        self.moveTo(location)
        assert button in self.MOUSE_BUTTONS.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
        button = self.MOUSE_BUTTONS[button]
        fake_input(self.display, X.ButtonPress, button)
        self.display.sync()

    def _mouseUp(self, location: Location, button: str):
        """
        Mouse button Up

        :param location :x,y coordinates where to click
        :param button 'left','middle','right'

        """
        self.moveTo(location)
        assert button in self.MOUSE_BUTTONS.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
        button = self.MOUSE_BUTTONS[button]
        fake_input(self.display, X.ButtonRelease, button)
        self.display.sync()

    def position(self):
        """Returns:
          (x, y) tuple of the current xy coordinates of the mouse cursor.
        """
        coord = self.display.screen().root.query_pointer()._data
        position = (coord["root_x"], coord["root_y"])
        return position
