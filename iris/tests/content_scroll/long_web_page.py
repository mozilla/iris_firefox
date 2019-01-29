# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly on long web pages.'
        self.test_case_id = '4660'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        scroll_content_pattern = Pattern('about_us_content.png')
        scroll_content_after_zoomed_in_pattern = Pattern('after_zoomed_in_content.png')
        after_scroll_content_pattern = Pattern('after_scroll_content.png')

        if Settings.is_windows():
            value = SCREEN_HEIGHT
        else:
            value = 10

        navigate('http://www.eginstill.com/')
        location_to_open = Location(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        time.sleep(DEFAULT_FIREFOX_TIMEOUT)
        click(location_to_open)

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists,
                    'The page content is loaded')
        click(scroll_content_pattern)

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_pattern, scroll, (-value, None), 100, DEFAULT_UI_DELAY)
        assert_true(self, after_scroll_content_exists,
                    'Scroll down using mouse wheel on the long web page is successful')

        [zoom_in() for _ in range(2)]

        after_scroll_content_exists = \
            scroll_until_pattern_found(scroll_content_after_zoomed_in_pattern, scroll, (value, None), 100, DEFAULT_UI_DELAY)
        assert_true(self, after_scroll_content_exists,
                    'Scroll up using mouse wheel after zooming is successful')
