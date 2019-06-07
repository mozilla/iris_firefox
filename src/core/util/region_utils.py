# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

from src.core.api.finder.finder import wait, exists, find
from src.core.api.screen.region import Region
from src.core.api.screen.screen import Screen
from src.core.api.location import Location
from src.core.api.errors import FindError

logger = logging.getLogger(__name__)


class RegionUtils:

    @staticmethod
    def generate_region_by_markers(top_left_marker_img=None, bottom_right_marker_img=None):
        """Generate a region starting from 2 markers.

        :param top_left_marker_img: Top left pattern used to generate the region.
        :param bottom_right_marker_img: Bottom right pattern used to generate the region.
        :return: Screen region generated.
        """
        try:
            wait(top_left_marker_img, 10)
            exists(bottom_right_marker_img, 10)
        except FindError:
            raise FindError('Unable to find page markers.')

        top_left_pos = find(top_left_marker_img)
        bottom_right_pos = find(bottom_right_marker_img)

        marker_width, marker_height = bottom_right_marker_img.get_size()

        return Region(top_left_pos.x,
                      top_left_pos.y,
                      (bottom_right_pos.x + marker_width),
                      bottom_right_pos.y - top_left_pos.y + marker_height)

    @staticmethod
    def create_region_from_patterns(top=None, bottom=None, left=None, right=None, padding_top=None, padding_bottom=None,
                                    padding_left=None, padding_right=None):
        """Returns a region created from combined area of one or more patterns. Argument names are just for convenience
        and don't influence outcome.

        :param top: Top pattern used to generate the region.
        :param bottom: Bottom pattern used to generate the region.
        :param left: Left pattern used to generate the region.
        :param right: Right pattern used to generate the region.
        :param padding_top: Padding to be added to the pattern's top.
        :param padding_bottom: Padding to be added to the pattern's bottom.
        :param padding_left: Padding to be added to the pattern's left.
        :param padding_right: Padding to be added to the pattern's right.
        :return: region created from combined area of one or more patterns.
        """

        patterns = []
        if top:
            patterns.append(top)
        if bottom:
            patterns.append(bottom)
        if left:
            patterns.append(left)
        if right:
            patterns.append(right)

        if len(patterns) == 0:
            raise ValueError('One or more patterns required.')

        logger.debug('Creating region from %s pattern(s).' % len(patterns))

        a, b = (Screen().width, Screen().height)
        p1 = Location(a, b)
        p2 = Location(0, 0)

        for pattern in patterns:
            if exists(pattern, 5):
                current_pattern = find(pattern)
                if current_pattern.x < p1.x:
                    p1.x = current_pattern.x
                if current_pattern.y < p1.y:
                    p1.y = current_pattern.y

                w, h = pattern.get_size()

                if current_pattern.x + w > p2.x:
                    p2.x = current_pattern.x + w
                if current_pattern.y + h > p2.y:
                    p2.y = current_pattern.y + h
            else:
                raise FindError('Pattern not found: %s ' % pattern)

        found_region = Region(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y)

        if padding_top or padding_bottom or padding_left or padding_right:
            logger.debug('Adding padding to region.')

        if padding_top:
            found_region.y -= padding_top
            found_region.height += padding_top

        if padding_bottom:
            found_region.height += padding_bottom

        if padding_left:
            found_region.x -= padding_left
            found_region.width += padding_left

        if padding_right:
            found_region.width += padding_right

        return found_region
