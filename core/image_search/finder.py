# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from typing import List

from core.errors import FindError
from core.helpers.location import Location
from core.helpers.rectangle import Rectangle
from core.image_search.image_search import image_find, match_template, match_template_multiple, image_vanish
from core.image_search.pattern import Pattern
from core.screen.display import Display
from core.settings import Settings


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
            #     highlight(region=region, pattern=ps, location=image_found)
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
            #     highlight(region=region, pattern=image_name, location=image_found)
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
