# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from core.helpers.location import Location
from core.mouse.mouse_utils import _mouse_press_release, _general_click, _to_location, _scroll, _drag_drop, \
    _click_delay, _move_mouse_delay


class Mouse:



    def mouse_press(self, where: type = None, button: str = None, in_region: type = None):
        """Mouse press. Wrapper over _mouse_press_release.

        :param where: Location , image name or Pattern.
        :param button: 'left','right' or 'middle'.
        :param in_region: Region object in order to minimize the area.
        :return: Call the _mouse_press_release() method with the 'press' option.
        """
        return _mouse_press_release(where, 'press', button, in_region)

    def mouse_release(self, where: type = None, button: str = None, in_region: type = None):
        """Mouse release. Wrapper over _mouse_press_release.

        :param where: Location , image name or Pattern.
        :param button: 'left','right' or 'middle'.
        :param in_region: Region object in order to minimize the area.
        :return: Call the _mouse_press_release() method with the 'release' option.
        """
        return _mouse_press_release(where, 'release', button, in_region)

    def mouse_move(self, where: type = None, duration: int = None, in_region: type = None):
        """Mouse move. Wrapper over _general_click.
        :param where: Location , image name or Pattern.
        :param duration: Speed of hovering from current location to target.
        :param in_region: Region object in order to minimize the area.
        :return: None.
        """
        if duration is None:
            duration = _move_mouse_delay()
        _general_click(where, 0, duration, in_region, 'left')

    def click(self, where: type = None, duration: int = None, in_region: type = None):
        """Mouse left click. Wrapper over _general_click.

        :param where: Location , image name or Pattern.
        :param duration: Speed of hovering from current location to target.
        :param in_region: Region object in order to minimize the area.
        :return: None.
        """

        if duration is None:
            duration = self.move_mouse_delay

        _general_click(where, 1, duration, in_region, 'left')

    def right_click(self, where: type = None, duration: int = None, in_region: type = None):
        """Mouse right click. Wrapper over _general_click.

        :param where: Location , image name or Pattern.
        :param duration: Speed of hovering from current location to target.
        :param in_region: Region object in order to minimize the area.
        :return: None.
        """

        if duration is None:
            duration = self.move_mouse_delay

        _general_click(where, 1, duration, in_region, 'right')

    def double_click(self, where: type = None, duration: int = None, in_region: type = None):
        """Mouse double click. Wrapper over _general_click.

        :param where: Location , image name or Pattern.
        :param duration: Speed of hovering from current location to target.
        :param in_region: Region object in order to minimize the area.
        :return: None.
        """

        if duration is None:
            duration = self.move_mouse_delay

        _general_click(where, 2, duration, in_region, 'left')

    def to_location(self, ps: type = None, in_region: type = None):
        """Transform pattern or string to location.

        :param ps: Pattern or string input.
        :param in_region: Region object in order to minimize the area.
        :param align: Alignment could be top_left, center.
        :return: Location object.
        """
        return _to_location(ps, in_region, 'top_left')

    def drag_drop(self, drag_from: type, drop_to: type, duration: int = None):
        """Mouse drag and drop.

        :param drag_from: Starting point for drag and drop. Can be pattern, string or location.
        :param drop_to: Ending point for drag and drop. Can be pattern, string or location.
        :param duration: Speed of drag and drop.
        :return: None.
        """
        return _drag_drop(drag_from, drop_to, duration)

    def scroll(self, clicks: int):
        """Performs a scroll of the mouse scroll wheel.

        :param clicks: The amount of scrolling to perform.
        :return: None.
        """
        return _scroll(clicks)


if __name__ == '__main__':
    m = Mouse()
    m.mouse_move(Location(100,100))