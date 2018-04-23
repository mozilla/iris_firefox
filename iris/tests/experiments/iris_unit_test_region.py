# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is an experiment for Pattern,Location and Region with chain operations'

    def run(self):
        url = 'https://www.google.com/?hl=EN'
        navigate(url)

        home_string = 'home.png'
        image_string = 'google_search.png'
        pattern = Pattern('google_search.png')

        wait(pattern)

        for x_margin in range(0, screen_width, 100):
            new_region = Region(x_margin, 0, 100, screen_height)

            hover(Location(x_margin, 0))

            new_region.find(Pattern(image_string))
            new_region.find(Pattern(home_string))
