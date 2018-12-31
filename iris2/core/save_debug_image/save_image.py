# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import datetime
import logging
import re

import cv2
import numpy as np

from iris2.core.finder.pattern import Pattern
from iris2.core.screen.screenshot_image import ScreenshotImage

try:
    import Image
except ImportError:
    from PIL import Image

logger = logging.getLogger(__name__)


def save_debug_image(needle, haystack, locations):
    """Saves input Image for debug.

    :param Image || None needle: Input needle image that needs to be highlighted.
    :param Image || Region haystack: Input Region as Image.
    :param List[Location] || Location locations: Location or list of Location as coordinates.
    :return: None.
    """

    if not isinstance(needle, Pattern):
        logger.warning('First parameter should be instance of Pattern')
        return

    if not isinstance(haystack, ScreenshotImage):
        logger.warning('Second parameter should be instance of ScreenshotImage or Region')
        return

    w, h = needle.get_size()
    temp_f = re.sub('[ :.-]', '_', str(datetime.datetime.now())) + ('_not_found' if len(locations) == 0 else '_found')
    file_name = '%s.jpg' % temp_f
    not_found_txt = ' <<< Pattern not found!'

    if len(locations) > 0:
        for loc in locations:
            cv2.rectangle(haystack.get_gray_array(), (loc.x, loc.y), (loc.x + w, loc.y + h), (0, 0, 255), 2)
        cv2.imwrite(file_name, haystack.get_gray_array(), [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    else:
        gray_img = haystack.get_gray_image()
        search_for_image = needle.get_color_image()
        v_align_pos = int(gray_img.size[1] / 2 - h / 2)

        d_image = Image.new("RGB", (gray_img.size[0], gray_img.size[1]))
        d_image.paste(gray_img)
        d_image.paste(search_for_image, (0, v_align_pos))
        d_array = np.array(d_image)
        cv2.rectangle(d_array, (w, v_align_pos), (haystack.width, v_align_pos + h), (255, 255, 255), cv2.FILLED)
        cv2.putText(d_array, not_found_txt, (w, v_align_pos + h - 5), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 1, 16)
        cv2.imwrite(file_name, d_array, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
