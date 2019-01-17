# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling with different settings at browser-level.'
        self.test_case_id = '4714'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        scroll_content_pattern = Pattern('about_us_content.png')

        navigate('http://www.eginstill.com/')

        location_to_open = Location(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        time.sleep(DEFAULT_FIREFOX_TIMEOUT)

        click(location_to_open)

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using mouse wheel is on the page')

        [scroll(-SCREEN_HEIGHT) for _ in range(10)]
        try:
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')
        [scroll(SCREEN_HEIGHT) for _ in range(10)]

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using mouse wheel is successful.')
