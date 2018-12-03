# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import time
from typing import List

from core.enums import Color
from core.errors import FindError
from core.helpers.location import Location
from core.helpers.rectangle import Rectangle
from core.highlight.screen_highlight import ScreenHighlight, HighlightRectangle
from core.image_search.image_search import image_find, match_template, match_template_multiple, image_vanish
from core.image_search.pattern import Pattern
from core.screen.display import Display
from core.settings import Settings


def highlight(region=None, seconds=None, color=None, pattern=None, location=None):
    """
    :param region: Screen region to be highlighted.
    :param seconds: How many seconds the region is highlighted. By default the region is highlighted for 2 seconds.
    :param color: Color used to highlight the region. Default color is red.
    :param pattern: Pattern.
    :param location: Location.
    :return: None.
    """
    if color is None:
        color = Settings.highlight_color

    if seconds is None:
        seconds = Settings.highlight_duration

    hl = ScreenHighlight()
    if region is not None:
        hl.draw_rectangle(HighlightRectangle(region.x, region.y, region.width, region.height, color))
        i = hl.canvas.create_text(region.x, region.y,
                                  anchor='nw',
                                  text='Region',
                                  font=("Arial", 12),
                                  fill=Color.WHITE.value)

        r = hl.canvas.create_rectangle(hl.canvas.bbox(i), fill=color, outline=color)
        hl.canvas.tag_lower(r, i)

    if pattern is not None:
        width, height = pattern.get_size()
        hl.draw_rectangle(HighlightRectangle(location.x, location.y, width, height, color))

    hl.render(seconds)
    time.sleep(seconds)


def find(ps: Pattern or str, region: Rectangle = None) -> Location or FindError:
    """Look for a single match of a Pattern or image.

    :param ps: Pattern or String.
    :param region: Rectangle object in order to minimize the area.
    :return: Location object.
    """
    if isinstance(ps, Pattern):
        if region is None:
            region = Display(1).bounds

        image_found = match_template(ps, region)
        if (image_found.x != -1) & (image_found.y != -1):
            # if parse_args().highlight:
            highlight(region=region, pattern=ps, location=image_found)
            return image_found
        else:
            raise FindError('Unable to find image %s' % ps.get_filename())
    # TODO OCR text search


def find_all(pattern: Pattern or str, region: Rectangle = None, threshold: float = 0.5) -> List[Location] or FindError:
    """Look for all matches of a Pattern or image.

    :param pattern: Pattern or String.
    :param region: Rectangle object in order to minimize the area.
    :param threshold: float that stores the minimum similarity.
    :return: Location object or FindError.
    """
    if region is None:
        region = Display(0).bounds

    images_found: List[Location] = match_template_multiple(pattern, region, threshold)
    if len(images_found) > 0:
        return images_found
    else:
        raise FindError('Unable to find image %s' % pattern.get_filename())


def wait(ps: Pattern or str, timeout: float = None, region: Rectangle = None) -> bool or FindError:
    """Wait for a Pattern or image to appear.

    :param ps: String or Pattern.
    :param timeout: Number as maximum waiting time in seconds.
    :param region: Rectangle object in order to minimize the area.
    :return: True if found, otherwise raise FindError.
    """
    if isinstance(ps, Pattern):
        if timeout is None:
            timeout = Settings.auto_wait_timeout

        if region is None:
            region = Display(0).bounds

        image_found = image_find(ps, timeout, region)
        if image_found is not None:
            # if parse_args().highlight:
            highlight(region=region, pattern=ps, location=image_found)
            return True
        else:
            raise FindError('Unable to find image %s' % ps.get_filename())
    # TODO OCR text search


def exists(ps: Pattern or str, timeout: float = None, region: Rectangle = None) -> bool:
    """Check if Pattern or image exists.

    :param ps: String or Pattern.
    :param timeout: Number as maximum waiting time in seconds.
    :param region: Rectangle object in order to minimize the area.
    :return: True if found.
    """

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    try:
        wait(ps, timeout, region)
        return True
    except FindError:
        return False


def wait_vanish(pattern: Pattern, timeout: float = None, region: Rectangle = None) -> bool or FindError:
    """Wait until a Pattern disappears.

    :param pattern: Pattern.
    :param timeout:  Number as maximum waiting time in seconds.
    :param region: Rectangle object in order to minimize the area.
    :return: True if vanished.
    """

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    if region is None:
        region = Display(0).bounds

    image_found = image_vanish(pattern, timeout, region)

    if image_found is not None:
        return True
    else:
        raise FindError('%s did not vanish' % pattern.get_filename())
