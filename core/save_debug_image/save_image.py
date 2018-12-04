# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import logging
import re

import cv2
import numpy as np

from core.finder.pattern import Pattern
from core.screen.screenshot_image import ScreenshotImage

try:
    import Image
except ImportError:
    from PIL import Image

logger = logging.getLogger(__name__)


def _debug_put_text(on_what, input_text='Text', start=(0, 0)):
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    scale = 1
    thickness = 1

    text_size = cv2.getTextSize(input_text, font, scale * 2, thickness)
    start_point = start or (0, 0)

    cv2.putText(on_what,
                input_text,
                (start_point[0], start_point[1] + text_size[0][1] - int(text_size[0][1] / 4)),
                font,
                scale,
                (0, 0, 0),
                thickness, 64)


def save_debug_image(needle, haystack, locations):
    """Saves input Image for debug.

    :param Image || None needle: Input needle image that needs to be highlighted.
    :param Image || Region haystack: Input Region as Image.
    :param List[Location] || Location || None locations: Location or list of Location as coordinates.
    :return: None.
    """

    if not isinstance(needle, Pattern):
        logger.warning('First parameter should be instance of Pattern')
        return

    if not isinstance(haystack, ScreenshotImage):
        logger.warning('Second parameter should be instance of ScreenshotImage or Region')

    w, h = needle.get_size()
    print('Width: %s, Height: %s' % (w, h))

    temp_f = re.sub('[ :.-]', '_', str(datetime.datetime.now())) + ('_not_found' if len(locations) == 0 else '')
    file_name = '%s.jpg' % temp_f

    def _draw_rectangle(on_what, top_x, top_y, btm_x, btm_y, width=2):
        cv2.rectangle(on_what, (top_x, top_y), (btm_x, btm_y), (0, 0, 255), width)

    if len(locations) > 0:
        for location in locations:
            _draw_rectangle(haystack.get_rgb_array(), location.x, location.y, location.x + w, location.y + h)

        cv2.imwrite(file_name, haystack.get_rgb_array(), [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    else:
        gray_img = haystack.get_gray_image()
        search_for_image = needle.get_color_image()

        tuple_paste_location = (0, int(gray_img.size[1] / 4))
        d_image = Image.new("RGB", (gray_img.size[0], gray_img.size[1]))
        d_image.paste(gray_img)
        d_image.paste(search_for_image, (0, 0))
        d_array = np.array(d_image)
        cv2.rectangle(d_array, (w, 0), (haystack.width, h), (255, 255, 255))
        _debug_put_text(d_array, '<<< Pattern not found', (search_for_image.size[0], tuple_paste_location[1]))
        d_image.show()
        cv2.imwrite(file_name, d_array, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
