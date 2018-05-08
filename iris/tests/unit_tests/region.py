# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is an experiment for Pattern,Location and Region with chain operations'
        # self.exclude = Platform.ALL

    def run(self):
        home_string = 'home.png'
        google = 'google_search.png'
        pattern = Pattern('google_search.png')

        url = 'https://www.google.com/?hl=EN'
        navigate(url)
        wait(pattern)

        new_region = Region(0, 0, screen_width, screen_height)
        new_region.wait(pattern)
        new_region.debug()

        quit_firefox()
        raise Exception('wtf')

        new_region.hover(pattern)
        new_region.hover(google)
        new_region.hover(Location(20, 20))

        new_region.hover(Pattern(home_string))
        new_region.hover(Pattern(home_string).targetOffset(15, 15))

        new_region.find(pattern)
        new_region.find(google)

        new_region.wait(pattern, 5)
        new_region.wait(google, 5)

        new_region.click(google, 0)
        new_region.click(pattern, 0)
        new_region.click(pattern.targetOffset(30, 5), 0)
        new_region.click(pattern.targetOffset(30, 10), 0)

        q_region = Region(0, 0, screen_width / 4, 200)
        q_region.debug()

        Region(0, 0, screen_width / 4, 200).click(Pattern('home.png').targetOffset(10, 10))

        navigate(url)
        wait(pattern)

        for x_margin in range(0, screen_width, 200):
            new_region = Region(x_margin, 0, 200, screen_height)

            hover(Location(x_margin, 0))

            new_region.find(Pattern(google))
            new_region.find(Pattern(home_string))
