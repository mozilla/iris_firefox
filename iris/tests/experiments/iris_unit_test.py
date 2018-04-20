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

        image_string = 'google_search.png'
        home_string = 'home.png'
        pattern = Pattern('google_search.png')

        wait(pattern)

        # >>> HOVER TEST <<<
        logger.info('>>> HOVER TEST <<<')

        hover(image_string)
        hover(Location(0, 0))
        hover(pattern)

        hover(pattern.targetOffset(20, 0))
        hover(pattern.targetOffset(30, 0))
        hover(pattern.targetOffset(40, 0))
        hover(pattern.targetOffset(50, 0))
        hover(pattern.targetOffset(100, 0))

        hover(Location(0, 0))

        # >>> FIND TEST <<<
        logger.info('>>> FIND TEST <<<')

        pos_by_name = find(image_string)
        assert_true(self, isinstance(pos_by_name, Location), 'Find by String should return Location')

        pos_by_pattern = find(pattern)
        assert_true(self, isinstance(pos_by_pattern, Location), 'Find by Pattern should return Location')

        # >>> WAIT TEST <<<
        logger.info('>>> WAIT TEST <<<')

        assert_true(self, wait(image_string, 10), 'Wait by String should return True')
        assert_true(self, wait(pattern, 10), 'Wait by Pattern should return True')

        # >>> EXISTS TEST <<<
        logger.info('>>> EXISTS TEST <<<')

        assert_true(self, exists(image_string), 'Exists by String should return True')
        assert_true(self, exists(pattern), 'Exists by Pattern should return True')

        # >>> CLICK AND VANISH TEST <<<
        logger.info('>>> CLICK AND VANISH TEST <<<')

        click(Location(0, 0))
        click(pos_by_name)
        click(home_string)
        assert_true(self, waitVanish(image_string), 'Google button should vanish')
        click('back.png')
        click(home_string)
        assert_true(self, waitVanish(pattern), 'Google button should vanish')
        click('back.png')

        click(pattern)
        click(pattern.targetOffset(10, 0))
        click(pattern.targetOffset(20, 0))
        click(pattern.targetOffset(30, 5))
        click(pattern.targetOffset(30, 10))

        # >>> BASED ON REGION EXAMPLES <<<
        logger.info('>>>BASED ON REGION EXAMPLES <<<')

        new_region = Region(0, 0, screen_width / 2, screen_height)

        new_region.hover(pattern)
        new_region.hover(image_string)
        new_region.hover(Location(20, 20))

        new_region.hover(Pattern('home.png'))
        new_region.hover(Pattern('home.png').targetOffset(15, 15))

        new_region.find(pattern)
        new_region.find(image_string)

        new_region.wait(pattern, 5)
        new_region.wait(image_string, 5)

        new_region.click(image_string)
        new_region.click(pattern)
        new_region.click(pattern.targetOffset(30, 5))
        new_region.click(pattern.targetOffset(30, 10))

        Region(0, 0, screen_width / 4, 200).click(Pattern('home.png').targetOffset(10, 10))
