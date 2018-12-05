# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import time

import pyautogui
from pynput.mouse import Controller, Button

from core.errors import FindError
from core.helpers.location import Location
from core.settings import *
from core.arg_parser import parse_args
from core.image_search.image_search import image_find
from core.image_search.pattern import Pattern

INVALID_GENERIC_INPUT = 'Invalid input'
INVALID_NUMERIC_INPUT = 'Expected numeric value'


def _click_delay():
    return Settings.DEFAULT_CLICK_DELAY

def _move_mouse_delay():
        return Settings.DEFAULT_MOVE_MOUSE_DELAY

@staticmethod
def _mouse_press_release(where: type = None, action: str = None, button: str = None, in_region: type = None):
    """Mouse press/release.

    :param where: Location , image name or Pattern.
    :param action: 'press' or 'release'.
    :param button: 'left','right' or 'middle'.
    :param in_region: Region object in order to minimize the area.
    :return: None.
    """
    if isinstance(where, Pattern):
        needle = cv2.imread(where.get_file_path())
        height, width, channels = needle.shape
        p_top = image_find(pattern=where, region=in_region)
        if p_top is None:
            raise FindError('Unable to click on: %s' % where.get_file_path())
        possible_offset = where.get_target_offset()
        if possible_offset is not None:
            location = Location(p_top.x + possible_offset.x, p_top.y + possible_offset.y)
            pyautogui.moveTo(location.x, location.y)
            if action == 'press':
                pyautogui.mouseDown(location.x, location.y, button)
            elif action == 'release':
                pyautogui.mouseUp(location.x, location.y, button)
        else:
            location = Location(p_top.x + width / 2, p_top.y + height / 2)
            pyautogui.moveTo(location.x, location.y)
            if action == 'press':
                pyautogui.mouseDown(location.x, location.y, button)
            elif action == 'release':
                pyautogui.mouseUp(location.x, location.y, button)
    elif isinstance(where, str):
        mouse = Controller()
        a_match = text_search_by(where, True, in_region)
        if a_match is not None:
            location = Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
            mouse.move(location.x, location.y)
            if action == 'press':
                mouse.press(button)
            elif mouse == 'release':
                mouse.release(button)

def _click_at(location: type = None, clicks: int = None, duration: int = None, button: int = None):
    """Click on Location coordinates.

    :param location: Location , image name or Pattern.
    :param clicks: Number of mouse clicks.
    :param duration: Speed of hovering from current location to target.
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3).
    :return: None.
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    if location is None:
        location = Location(0, 0)

    pyautogui.moveTo(location.x, location.y, duration)
    if parse_args().highlight:
        print("a")
        # hl = ScreenHighlight()
        # hl.draw_circle(HighlightCircle(location.x, location.y, 15))
        # hl.render()
    if clicks > 1:
        mouse = Controller()
        mouse.position = (location.x, location.y)
        mouse.click(Button.left, 2)
    else:
        pyautogui.click(clicks=clicks, interval=Settings.click_delay, button=button)

    if Settings.click_delay != _click_delay():
        Settings.click_delay = _click_delay()

@staticmethod
def _click_pattern(pattern: Pattern, clicks: int = None, duration: int = None, in_region: type = None,
                   button: int = None):
    """Click on center or offset of a Pattern.

    :param pattern: Input Pattern.
    :param clicks: Number of mouse clicks.
    :param duration: Speed of hovering from current location to target.
    :param in_region: Region object in order to minimize the area.
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3).
    :return: None.
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    needle = cv2.imread(pattern.get_file_path())
    height, width, channels = needle.shape

    p_top = image_find(pattern=pattern, region=in_region)

    if p_top is None:
        raise FindError('Unable to click on: %s' % pattern.get_file_path())

    possible_offset = pattern.get_target_offset()

    if possible_offset is not None:
        _click_at(Location(p_top.x + possible_offset.x, p_top.y + possible_offset.y), clicks, duration, button)
    else:
        _click_at(Location(p_top.x + width / 2, p_top.y + height / 2), clicks, duration, button)

def _general_click(where: type = None, clicks: int = None, duration: int = None, in_region=None, button: str = None):
    """General Mouse Click.

    :param where: Location , image name or Pattern.
    :param clicks: Number of mouse clicks.
    :param duration: Speed of hovering from current location to target.
    :param in_region: Region object in order to minimize the area.
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3).
    :return: None.
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    if isinstance(where, Pattern):
        _click_pattern(where, clicks, duration, in_region, button)

    elif isinstance(where, str):
        print('Need OCR update')
        # a_match = text_search_by(where, True, in_region)
        # if a_match is not None:
        #     click_location = Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        #     _click_at(click_location, clicks, duration, button)

    elif isinstance(where, Location):
        _click_at(where, clicks, duration, button)

    else:
        raise ValueError("")


def _to_location(ps=None, in_region=None, align: str = 'top_left'):
    """Transform pattern or string to location.

    :param ps: Pattern or string input.
    :param in_region: Region object in order to minimize the area.
    :param align: Alignment could be top_left, center.
    :return: Location object.
    """
    if isinstance(ps, Location):
        return ps

    elif isinstance(ps, Pattern):
        location = image_find(ps, in_region)
        width, height = ps.get_size()
        if align == 'center':
            return Location(location.x + width / 2, location.y + height / 2)
        elif align == 'top_right':
            return Location(location.x + width, location.y)
        elif align == 'bottom_left':
            return Location(location.x, location.y + height)
        elif align == 'bottom_right':
            return Location(location.x + width, location.y + height)
        else:
            return location

def _scroll(clicks):
    pyautogui.scroll(clicks)


def _drag_drop(self, drag_from: type, drop_to: type, duration: int = None):
    """Mouse drag and drop.

    :param drag_from: Starting point for drag and drop. Can be pattern, string or location.
    :param drop_to: Ending point for drag and drop. Can be pattern, string or location.
    :param duration: Speed of drag and drop.
    :return: None.
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    # Ensure Iris has time to get correct target coordinates before initiating DnD.
    time.sleep(Settings.UI_DELAY)
    from_location = _to_location(ps=drag_from)
    self._to_location = _to_location(ps=drop_to)
    pyautogui.moveTo(from_location.x, from_location.y, 0)

    time.sleep(Settings.delay_before_mouse_down)
    pyautogui.mouseDown(button='left', _pause=False)

    time.sleep(Settings.delay_before_drag)
    pyautogui._mouseMoveDrag('drag', _to_location.x, _to_location.y, 0, 0, duration, pyautogui.linear, 'left')

    time.sleep(Settings.delay_before_drop)
    pyautogui.mouseUp(button='left', _pause=False)
