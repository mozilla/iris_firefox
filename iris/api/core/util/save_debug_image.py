# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import os
import re

import cv2
import numpy as np

try:
    import Image
except ImportError:
    from PIL import Image

from core_helper import IrisCore
from iris.api.core.location import Location


def _debug_put_text(on_what, input_text='Text', start=(0, 0)):
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    scale = 1
    thickness = 1

    text_size = cv2.getTextSize(input_text, font, scale * 2, thickness)
    start_point = start or (0, 0)
    cv2.rectangle(on_what,
                  start_point,
                  (start_point[0] + text_size[0][0], start_point[1] + text_size[0][1]),
                  (0, 0, 0),
                  cv2.FILLED)

    cv2.putText(on_what,
                input_text,
                (start_point[0], start_point[1] + text_size[0][1] - text_size[0][1] / 4),
                font,
                scale,
                (255, 255, 255),
                thickness, 64)


def save_debug_image(needle, haystack, locations, not_found=False):
    """Saves input Image for debug.

    :param Image || None needle: Input needle image that needs to be highlighted.
    :param Image || Region haystack: Input Region as Image.
    :param List[Location] || Location || None locations: Location or list of Location as coordinates.
    :param not_found: boolean if image was found or not.
    :return: None.
    """
    test_name = IrisCore.get_test_name()

    if test_name is not None:
        is_image = False if isinstance(needle, str) and IrisCore.is_ocr_text(needle) else True
        w, h = 0, 0

        try:
            full_screen = IrisCore.get_region(haystack)
            haystack = np.array(Image.fromarray(np.array(full_screen)).convert('L'))
        except Exception:
            if haystack is not None:
                haystack = np.array(Image.fromarray(np.array(haystack)).convert('RGB'))
            else:
                haystack = IrisCore.get_region(None)

        if needle is None:
            h, w = haystack.shape
        elif is_image:
            w, h = np.array(needle).shape[::-1]

        temp_f = re.sub('[ :.-]', '_', str(datetime.datetime.now())) + '_' + test_name.replace('.py', '')

        def _draw_rectangle(on_what, (top_x, top_y), (btm_x, btm_y), width=2):
            cv2.rectangle(on_what, (top_x, top_y), (btm_x, btm_y), (0, 0, 255), width)

        if locations is None:
            if not_found:
                locations = Location(0, 0)
            else:
                temp_f = temp_f + '_debug'
                region_ = Image.fromarray(haystack).size
                try:
                    haystack = cv2.cvtColor(haystack, cv2.COLOR_GRAY2RGB)
                except Exception:
                    pass
                if is_image:
                    _draw_rectangle(haystack, (0, 0), (region_[0], region_[1]), 5)

        if not_found:
            temp_f = temp_f + '_not_found'

            on_region_image = Image.fromarray(haystack)
            if is_image:
                search_for_image = Image.fromarray(np.array(needle))

            tuple_paste_location = (0, on_region_image.size[1] / 4)

            d_image = Image.new("RGB", (on_region_image.size[0], on_region_image.size[1]))
            d_image.paste(on_region_image)
            if is_image:
                d_image.paste(search_for_image, tuple_paste_location)

            d_array = np.array(d_image)

            locations = Location(0, tuple_paste_location[1])

            if is_image:
                _debug_put_text(d_array, '<<< Pattern not found',
                                (search_for_image.size[0] + 10, tuple_paste_location[1]))
            else:
                _debug_put_text(d_array, '<<< Text not found: ' + needle, tuple_paste_location)
            haystack = d_array

        if isinstance(locations, list):
            for location in locations:
                if isinstance(location, Location):
                    _draw_rectangle(haystack, (location.x, location.y), (location.x + w, location.y + h))

        elif isinstance(locations, Location):
            _draw_rectangle(haystack, (locations.x, locations.y), (locations.x + w, locations.y + h))

        if not os.path.exists(IrisCore.get_image_debug_path()):
            os.mkdir(IrisCore.get_image_debug_path())
        file_name = os.path.join(IrisCore.get_image_debug_path(), '%s.jpg' % temp_f)
        cv2.imwrite(file_name, haystack, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
