# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is an experiment for OCR in region'

    def run(self):
        url = 'https://www.google.com/?hl=EN'
        navigate(url)

        pattern = Pattern('google_search.png')

        wait(pattern)

        for x_margin in range(0, screen_width / 4, 100):
            new_region = Region(x_margin, 0, 200, screen_height)

            hover(Location(x_margin, 0))
            text_data = new_region.text()

            for match in text_data:
                logger.info(match)

                # Hover over top left corner of text found
                hover(Location(match['x'], match['y']))

                # Hover over bottom right corner of text found
                hover(Location(match['x'] + match['width'], match['y'] + match['height']))
