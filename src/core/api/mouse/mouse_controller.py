# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import time

from pynput.mouse import Controller as MouseController, Button

from src.core.api.settings import Settings
from src.core.api.location import Location


def _get_point_on_line(x1, y1, x2, y2, n):
    """Returns the (x, y) tuple of the point that has progressed a proportion
    n along the line defined by the two x, y coordinates.
    """
    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    return x, y


class Mouse:
    def __init__(self):
        self.mouse = MouseController()

    def move(self, location: Location = None, duration: float = None):
        """Mouse move with tween.

        :param location: Location , image name or Pattern.
        :param duration: Speed of mouse movement from current mouse location to target.
        :return: None.
        """

        if location is None:
            location = Location(0, 0)

        if duration is None:
            duration = Settings.move_mouse_delay

        def set_mouse_position(loc_x, loc_y):
            self.mouse.position = (int(loc_x), int(loc_y))

        def smooth_move_mouse(from_x, from_y, to_x, to_y):
            num_steps = int(duration / 0.05)
            sleep_amount = 0
            try:
                sleep_amount = duration / num_steps
            except ZeroDivisionError:
                pass

            steps = [
                _get_point_on_line(from_x, from_y, to_x, to_y, n / num_steps)
                for n in range(num_steps)
            ]

            steps.append((to_x, to_y))
            for tween_x, tween_y in steps:
                tween_x = int(round(tween_x))
                tween_y = int(round(tween_y))
                set_mouse_position(tween_x, tween_y)
                time.sleep(sleep_amount)

        return smooth_move_mouse(
            self.mouse.position[0],
            self.mouse.position[1],
            location.x,
            location.y
        )

    def press(self, location: Location = None, duration: float = None, button: Button = Button.left):
        """Mouse press.

        :param location: Mouse press location.
        :param duration: Speed of mouse movement from current mouse location to target.
        :param button: 'left','right' or 'middle'.
        :return: None
        """
        self.move(location, duration)
        self.mouse.press(button)

    def release(self, location: Location = None, duration: float = None, button: Button = Button.left):
        """Mouse press.

        :param location: Mouse press location.
        :param duration: Speed of mouse movement from current mouse location to target.
        :param button: 'left','right' or 'middle'.
        :return: None
        """
        self.move(location, duration)
        self.mouse.release(button)

    def general_click(self, location: Location = None, duration: float = None, button: Button = Button.left,
                      clicks: int = 1):
        """General mouse click location.

        :param location: click location
        :param duration: Speed of mouse movement from current mouse location to target.
        :param button: 'left','right' or 'middle'.
        :param clicks: number of mouse clicks.
        :return: None.
        """
        self.move(location, duration)
        self.mouse.click(button, clicks)

    def drag_and_drop(self, start: Location, end: Location, duration: float = None):
        """Mouse drag and drop.

        :param start: Starting location
        :param end: Drop location
        :param duration: Speed of mouse movement to the drag and drop location.
        :return: None.
        """
        time.sleep(Settings.UI_DELAY)
        self.move(start, duration)
        time.sleep(Settings.delay_before_mouse_down)
        self.mouse.press(Button.left)
        time.sleep(Settings.delay_before_drag)
        self.move(end, duration)
        time.sleep(Settings.delay_before_drop)
        self.mouse.release(Button.left)

    def scroll(self, dx: int = None, dy: int = None, iterations: int = 1):
        """Sends scroll events.

        :param int dx: The horizontal scroll.
        :param int dy: The vertical scroll.
        :param int iterations: Number of iterations for the scroll event.
        :return None.
        """
        if dx is None:
            dx = Settings.mouse_scroll_step

        if dy is None:
            dy = Settings.mouse_scroll_step

        for i in range(iterations):
            self.mouse.scroll(dx, dy)
            time.sleep(0.5)
