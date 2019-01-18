# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import time
from typing import List

from src.core.api.arg_parser import parse_args
from src.core.api.enums import Color
from src.core.api.enums import MatchTemplateType
from src.core.api.errors import FindError
from src.core.api.finder.image_search import image_find, match_template, image_vanish
from src.core.api.finder.pattern import Pattern
from src.core.api.finder.text_search import text_find, text_find_all
from src.core.api.highlight.screen_highlight import ScreenHighlight, HighlightRectangle
from src.core.api.location import Location
from src.core.api.rectangle import Rectangle
from src.core.api.settings import Settings


def highlight(region=None, seconds=None, color=None, ps=None, location=None, text_location=None):
    """
    :param region: Screen region to be highlighted.
    :param seconds: How many seconds the region is highlighted. By default the region is highlighted for 2 seconds.
    :param color: Color used to highlight the region. Default color is red.
    :param ps: Pattern or str.
    :param location: pattern Location.
    :param text_location: list of Rectangles with text occurrences.
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

    if ps is not None:
        if isinstance(ps, Pattern):
            width, height = ps.get_size()
            for loc in location:
                hl.draw_rectangle(HighlightRectangle(loc.x, loc.y, width, height, color))
        elif isinstance(ps, str):
            for loc in text_location:
                hl.draw_rectangle(HighlightRectangle(loc.x, loc.y, loc.width, loc.height, color))

    hl.render(seconds)
    time.sleep(seconds)


def find(ps: Pattern or str, region: Rectangle = None) -> Location or FindError:
    """Look for a single match of a Pattern or image.

    :param ps: Pattern or String.
    :param region: Rectangle object in order to minimize the area.
    :return: Location object.
    """
    if isinstance(ps, Pattern):
        image_found = match_template(ps, region, MatchTemplateType.SINGLE)
        if len(image_found) > 0:
            if parse_args().highlight:
                highlight(region=region, ps=ps, location=image_found)
            return image_found[0]
        else:
            raise FindError('Unable to find image %s' % ps.get_filename())
    elif isinstance(ps, str):
        text_found = text_find(ps, region)
        if len(text_found) > 0:
            if parse_args().highlight:
                highlight(region=region, ps=ps, text_location=text_found)
            return Location(text_found[0].x, text_found[0].y)
        else:
            raise FindError('Unable to find text %s' % ps)


def find_all(ps: Pattern or str, region: Rectangle = None) -> List[Location] or FindError:
    """Look for all matches of a Pattern or image.

    :param ps: Pattern or String.
    :param region: Rectangle object in order to minimize the area.
    :return: Location object or FindError.
    """
    if isinstance(ps, Pattern):
        images_found: List[Location] = match_template(ps, region, MatchTemplateType.MULTIPLE)
        if len(images_found) > 0:
            if parse_args().highlight:
                highlight(region=region, ps=ps, location=images_found)
            return images_found
        else:
            raise FindError('Unable to find image %s' % ps.get_filename())
    elif isinstance(ps, str):
        locations = []
        text_found = text_find_all(ps, region)
        if len(text_found) > 0:
            if parse_args().highlight:
                highlight(region=region, ps=ps, text_location=text_found)
            for text in text_found:
                locations.append(Location(text.x, text.y))
                return locations
        else:
            raise FindError('Unable to find text %s' % ps)


def wait(ps: Pattern or str, timeout: float = None, region: Rectangle = None) -> bool or FindError:
    """Verify that a Pattern or str appears.

    :param ps: String or Pattern.
    :param timeout: Number as maximum waiting time in seconds.
    :param region: Rectangle object in order to minimize the area.
    :return: True if found, otherwise raise FindError.
    """
    if isinstance(ps, Pattern):
        if timeout is None:
            timeout = Settings.auto_wait_timeout

        image_found = image_find(ps, timeout, region)
        if image_found is not None:
            if parse_args().highlight:
                highlight(region=region, ps=ps, location=image_found)
            return True
        else:
            raise FindError('Unable to find image %s' % ps.get_filename())
    elif isinstance(ps, str):
        text_found = text_find(ps, region)
        if len(text_found) > 0:
            if parse_args().highlight:
                highlight(region=region, ps=ps, text_location=text_found)
            return Location(text_found[0].x, text_found[0].y)
        else:
            raise FindError('Unable to find text %s' % ps)
    else:
        raise ValueError('Invalid input')


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

    image_found = image_vanish(pattern, timeout, region)

    if image_found is not None:
        return True
    else:
        raise FindError('%s did not vanish' % pattern.get_filename())
