# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from src.core.api.enums import Alignment
from src.core.api.errors import FindError
from src.core.api.finder.image_search import image_find
from src.core.api.finder.pattern import Pattern
from src.core.api.mouse.mouse_controller import Mouse
from src.core.api.rectangle import Rectangle

try:
    from src.core.api.mouse.mouse_controller import Button
except AttributeError:
    from src.core.api.enums import Button


def move(ps: Pattern or str, duration: int = None, region: Rectangle = None, align: Alignment = None):
    """Mouse Move.

    :param ps: Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """
    click_location = None
    if isinstance(ps, Pattern):
        click_location = _get_pattern_click_location(ps, region, align)

    Mouse().move(click_location, duration)


def press(ps: Pattern or str, duration: int = None, region: Rectangle = None, button: Button = Button.left,
          align: Alignment = None):
    """Mouse Press.

    :param ps: Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param button: 'left','right' or 'middle'.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """
    click_location = None
    if isinstance(ps, Pattern):
        click_location = _get_pattern_click_location(ps, region, align)

    Mouse().press(click_location, duration, button)


def release(ps: Pattern or str, duration: int = None, region: Rectangle = None, button: Button = Button.left,
            align: Alignment = None):
    """Mouse Release.

    :param ps: Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param button: 'left','right' or 'middle'.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """
    click_location = None
    if isinstance(ps, Pattern):
        click_location = _get_pattern_click_location(ps, region, align)

    Mouse().release(click_location, duration, button)


def click(ps: Pattern or str = None, duration: int = None, region: Rectangle = None, align: Alignment = None):
    """Mouse Left Click.

    :param ps: Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """

    click_location = None
    if isinstance(ps, Pattern):
        click_location = _get_pattern_click_location(ps, region, align)

    Mouse().general_click(click_location, duration, Button.left, 1)


def right_click(ps: Pattern or str = None, duration: int = None, region: Rectangle = None, align: Alignment = None):
    """Mouse Right Click.

    :param ps: Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """

    click_location = None
    if isinstance(ps, Pattern):
        click_location = _get_pattern_click_location(ps, region, align)

    Mouse().general_click(click_location, duration, Button.right, 1)


def double_click(ps: Pattern or str = None, duration: int = None, region: Rectangle = None, align: Alignment = None):
    """Mouse Double Click.

    :param ps: Pattern or String.
    :param duration: Speed of hovering from current location to target.
    :param region: Region object in order to minimize the area.
    :param align: Click location alignment could be top_left, center, top_right, bottom_left, bottom_right.
    :return: None.
    """

    click_location = None
    if isinstance(ps, Pattern):
        click_location = _get_pattern_click_location(ps, region, align)

    Mouse().general_click(click_location, duration, Button.left, 2)


def drag_drop(drag_from: Pattern or str, drop_to: Pattern or str, region: Rectangle = None, duration: float = None,
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

    if isinstance(drag_from, Pattern):
        loc_to = _get_pattern_click_location(drop_to, region, align)

    Mouse().drag_and_drop(loc_from, loc_to, duration)

def mouse_reset():
    """Reset Mouse to coordinates to top left corner."""

    Mouse.move(0,0)

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
