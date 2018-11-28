# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from typing import List

from core.errors import FindError
from core.image_search.image_search import image_search_find, match_template, match_template_multiple
from core.image_search.pattern import Pattern
from core.settings import Settings
from core.helpers.location import Location
from core.screen.display import Display


def find(ps, region=None):
    """Look for a single match of a Pattern or image.

    :param ps: Pattern or String.
    :param region: Region object in order to minimize the area.
    :return: Location object.
    """
    if isinstance(ps, Pattern):
        if region is None:
            region = Display(1).bounds

        print(region)
        image_found = match_template(ps, region)
        if (image_found.x != -1) & (image_found.y != -1):
            # if parse_args().highlight:
            #     highlight(region=region, pattern=ps, location=image_found)
            return image_found
        else:
            raise FindError('Unable to find image %s' % ps.get_filename())


def find_all(pattern, region=None, threshold: float = 0.5) -> List[Location] or FindError:
    """Look for all matches of a Pattern or image.

    :param pattern: Pattern or String.
    :param region: Region object in order to minimize the area.
    :param threshold: float.
    :return: Location object.
    """
    if region is None:
        region = Display(0).bounds

    images_found: List[Location] = match_template_multiple(pattern, region, threshold)
    if len(images_found) > 0:
        return images_found
    else:
        raise FindError('Unable to find image %s' % pattern.get_filename())


def wait(image_name, timeout=None, region=None):
    """Wait for a Pattern or image to appear.

    :param image_name: String or Pattern.
    :param timeout: Number as maximum waiting time in seconds.
    :param region: Region object in order to minimize the area.
    :return: True if found.
    """
    if isinstance(image_name, Pattern):
        if timeout is None:
            timeout = Settings.auto_wait_timeout

        if region is None:
            region = Display(0).bounds

        image_found = image_search_find(image_name, timeout, region)
        if image_found is not None:
            # if parse_args().highlight:
            #     highlight(region=region, pattern=image_name, location=image_found)
            return True
        else:
            raise FindError('Unable to find image %s' % image_name.get_filename())


def exists(pattern, timeout=None, in_region=None):
    """Check if Pattern or image exists.

    :param pattern: String or Pattern.
    :param timeout: Number as maximum waiting time in seconds.
    :param in_region: Region object in order to minimize the area.
    :return: True if found.
    """

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    try:
        wait(pattern, timeout, in_region)
        return True
    except FindError:
        return False
