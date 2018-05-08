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
        url = 'https://www.google.com/?hl=EN'
        navigate(url)

        google = 'google_search.png'
        google_pattern = Pattern('google_search.png')
        home_button = 'home.png'
        back_button = 'back.png'

        wait(google_pattern)

        # >>> HOVER TEST <<<
        logger.info('>>> HOVER TEST <<<')

        hover(google)
        hover(Location(0, 0))
        hover(google_pattern)

        hover(google_pattern.targetOffset(20, 0))
        hover(google_pattern.targetOffset(30, 0))
        hover(google_pattern.targetOffset(40, 0))
        hover(google_pattern.targetOffset(50, 0))
        hover(google_pattern.targetOffset(100, 0))

        hover(google_pattern.targetOffset(-100, -1), 2)
        hover(google_pattern.targetOffset(-150, -2), 2)
        hover(google_pattern.targetOffset(-200, -3), 2)
        hover(google_pattern.targetOffset(-250, -4), 2)
        hover(google_pattern.targetOffset(-300, -5), 2)
        hover(google_pattern.targetOffset(-350, -6), 2)
        hover(google_pattern.targetOffset(-400, -7), 2)

        hover(Location(0, 0))

        # >>> FIND TEST <<<
        logger.info('>>> FIND TEST <<<')

        google_position = find(google)
        assert_true(self, isinstance(google_position, Location), 'Find by String should return Location')

        pos_by_pattern = find(google_pattern)
        assert_true(self, isinstance(pos_by_pattern, Location), 'Find by Pattern should return Location')

        # >>> WAIT TEST <<<
        logger.info('>>> WAIT TEST <<<')

        assert_true(self, wait(google, 10), 'Wait by String should return True')
        assert_true(self, wait(google_pattern, 10), 'Wait by Pattern should return True')

        # >>> EXISTS TEST <<<
        logger.info('>>> EXISTS TEST <<<')

        assert_true(self, exists(google), 'Exists by String should return True')
        assert_true(self, exists(google_pattern), 'Exists by Pattern should return True')

        # >>> CLICK AND VANISH TEST <<<
        logger.info('>>> CLICK AND VANISH TEST <<<')

        click(Location(0, 0))
        click(google_position, 0)
        click(home_button, 0)
        assert_true(self, waitVanish(google), 'Google button should vanish')
        click(back_button, 0)
        click(home_button, 0)
        assert_true(self, waitVanish(google_pattern), 'Google button should vanish')
        click(Pattern(back_button), 0)

        click(google_pattern, 0)
        click(google_pattern.targetOffset(10, 0), 0)
        click(google_pattern.targetOffset(20, 0), 0)
        click(google_pattern.targetOffset(30, 5), 0)
        click(google_pattern.targetOffset(30, 10), 0)


