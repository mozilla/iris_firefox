# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from core.errors import FindError
from core.image_search.image_search import image_search_find
from core.image_search.pattern import Pattern
from core.settings import Settings


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

        image_found = image_search_find(image_name, timeout, region)
        print(image_found)
        if image_found is not None:
            # if parse_args().highlight:
            #     highlight(region=region, pattern=image_name, location=image_found)
            return True
        else:
            raise FindError('Unable to find image %s' % image_name.get_filename())
