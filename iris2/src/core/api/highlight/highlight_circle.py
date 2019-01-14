# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris2.src.core.api.enums import Color
from iris2.src.core.api.settings import Settings


class HighlightCircle:
    def __init__(self, center_x: int, center_y: int, radius: int, color: Color = None, thickness: int = None):

        if thickness is None:
            thickness = Settings.highlight_thickness

        if color is None:
            color = Settings.highlight_color

        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color
        self.thickness = thickness
