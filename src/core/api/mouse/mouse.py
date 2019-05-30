# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import pyautogui as pyautogui

from src.core.api.enums import Alignment
from src.core.api.errors import FindError
from src.core.api.finder.image_search import image_find
from src.core.api.finder.pattern import Pattern
from src.core.api.finder.text_search import text_find
from src.core.api.location import Location
from src.core.api.mouse.mouse_controller import Mouse
from src.core.api.rectangle import Rectangle

try:
    from src.core.api.mouse.mouse_controller import Button
except AttributeError:
    from src.core.api.enums import Button


def move(lps: Location or Pattern or str, duration: int = None, region: Rectangle = None, align: Alignment = None):
    """Mouse Move.

    :param lps: Location or Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """
    click_location = None
    if isinstance(lps, Pattern):
        click_location = _get_pattern_click_location(lps, region, align)
    elif isinstance(lps, str):
        click_location = _get_string_click_location(lps, region, align)
    else:
        click_location = lps

    Mouse().move(click_location, duration)


def hover(lps: Location or Pattern or str = None, region: Rectangle = None, align: Alignment = None):
    """Mouse Hover.

    :param lps: Location or Pattern or String.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """
    move(lps, 1, region, align)


def press(lps: Location or Pattern or str, duration: int = None, region: Rectangle = None, button: Button = Button.left,
          align: Alignment = None):
    """Mouse Press.

    :param lps: Location or Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param button: 'left','right' or 'middle'.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """
    click_location = None
    if isinstance(lps, Pattern):
        click_location = _get_pattern_click_location(lps, region, align)
    elif isinstance(lps, str):
        click_location = _get_string_click_location(lps, region, align)
    else:
        click_location = lps

    Mouse().press(click_location, duration, button)


def release(lps: Location or Pattern or str, duration: int = None, region: Rectangle = None,
            button: Button = Button.left, align: Alignment = None):
    """Mouse Release.

    :param lps: Location or Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param button: 'left','right' or 'middle'.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """
    click_location = None
    if isinstance(lps, Pattern):
        click_location = _get_pattern_click_location(lps, region, align)
    elif isinstance(lps, str):
        click_location = _get_string_click_location(lps, region, align)
    else:
        click_location = lps

    Mouse().release(click_location, duration, button)


def click(lps: Location or Pattern or str = None, duration: int = None, region: Rectangle = None,
          align: Alignment = None):
    """Mouse Left Click.

    :param lps: Location or Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """

    click_location = None
    if isinstance(lps, Pattern):
        click_location = _get_pattern_click_location(lps, region, align)
    elif isinstance(lps, str):
        click_location = _get_string_click_location(lps, region, align)
    else:
        click_location = lps

    Mouse().general_click(click_location, duration, Button.left, 1)


def right_click(lps: Location or Pattern or str = None, duration: int = None, region: Rectangle = None,
                align: Alignment = None):
    """Mouse Right Click.

    :param lps: Location or Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """

    click_location = None
    if isinstance(lps, Pattern):
        click_location = _get_pattern_click_location(lps, region, align)
    elif isinstance(lps, str):
        click_location = _get_string_click_location(lps, region, align)
    else:
        click_location = lps

    Mouse().general_click(click_location, duration, Button.right, 1)


def double_click(lps: Location or Pattern or str = None, duration: int = None, region: Rectangle = None,
                 align: Alignment = None):
    """Mouse Double Click.

    :param lps: Location or Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """

    click_location = None
    if isinstance(lps, Pattern):
        click_location = _get_pattern_click_location(lps, region, align)
    elif isinstance(lps, str):
        click_location = _get_string_click_location(lps, region, align)
    else:
        click_location = lps

    Mouse().general_click(click_location, duration, Button.left, 2)


def middle_click(lps: Location or Pattern or str = None, duration: int = None, region: Rectangle = None,
                 align: Alignment = None):
    """Mouse middle click. Wrapper over _general_click.

    :param lps: Location or Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """

    click_location = None
    if isinstance(lps, Pattern):
        click_location = _get_pattern_click_location(lps, region, align)
    elif isinstance(lps, str):
        click_location = _get_string_click_location(lps, region, align)
    else:
        click_location = lps

    Mouse().general_click(click_location, duration, Button.middle, 1)


def drag_drop(drag_from: Location or Pattern or str, drop_to: Location or Pattern or str, region: Rectangle = None,
              duration: float = None,
              align: Alignment = None):
    """Mouse drag and drop.

    :param drag_from: Starting point for drag and drop. Can be pattern, string or location.
    :param drop_to: Ending point for drag and drop. Can be pattern, string or location.
    :param region: Region object in order to minimize the area.
    :param duration: Speed of drag and drop.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """
    loc_from = None
    loc_to = None

    if isinstance(drag_from, Pattern):
        loc_from = _get_pattern_click_location(drag_from, region, align)
    if isinstance(drag_from, str):
        loc_from = _get_string_click_location(drag_from, region, align)
    if isinstance(drag_from, Location):
        loc_from = drag_from

    if isinstance(drop_to, Pattern):
        loc_to = _get_pattern_click_location(drop_to, region, align)
    if isinstance(drop_to, str):
        loc_to = _get_string_click_location(drop_to, region, align)
    if isinstance(drop_to, Location):
        loc_to = drop_to

    Mouse().drag_and_drop(loc_from, loc_to, duration)


def mouse_reset():
    """Reset Mouse coordinates to top left corner."""

    Mouse().move(None, duration=0)


def scroll_down(dy: int = None, iterations: int = 1):
    """Scroll down mouse event."""
    Mouse().scroll(0, -abs(dy), iterations)


def scroll_up(dy: int = None, iterations: int = 1):
    """Scroll up mouse event."""
    Mouse().scroll(0, abs(dy), iterations)


def scroll_left(dx: int = None, iterations: int = 1):
    """Scroll left mouse event."""
    Mouse().scroll(-abs(dx), 0, iterations)


def scroll_right(dx: int = None, iterations: int = 1):
    """Scroll right mouse event."""
    Mouse().scroll(abs(dx), 0, iterations)


def scroll(clicks):
    """Performs a scroll of the mouse scroll wheel.
    :param clicks: The amount of scrolling to perform.
    :return: None.
    """
    pyautogui.scroll(clicks)


def _get_pattern_click_location(ps: Pattern, region: Rectangle = None, align: Alignment = None):
    """Returns the click location based on the pattern/string found location and alignment."""
    if align is None:
        align = Alignment.CENTER

    width, height = ps.get_size()
    find_location = image_find(ps, region=region)

    if find_location is None:
        raise FindError('Unable to click on: %s' % ps.get_file_path())

    if ps.get_target_offset():
        target_offset = ps.get_target_offset()
        find_location.x += target_offset.x
        find_location.y += target_offset.y

    rect = Rectangle(find_location.x, find_location.y, width, height)
    return rect.apply_alignment(align)


def _get_string_click_location(ps: str, region: Rectangle = None, align: Alignment = None):
    if align is None:
        align = Alignment.CENTER

    find_location = text_find(ps, region)

    if len(find_location) == 0:
        raise FindError('Unable to click on: %s' % ps)

    return find_location[0].apply_alignment(align)
