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
        after_scroll_content_pattern = Pattern('after_scroll_content.png')

        if Settings.is_windows():
            value = SCREEN_HEIGHT/2
        else:
            value = 10

        # Mousewheel scrolling preference is 200
        change_preference('mousewheel.default.delta_multiplier_y', '200')

        same_value_exists = check_preference('mousewheel.default.delta_multiplier_y', '200')
        assert_true(self, same_value_exists, 'The value is changed to 200')
        close_tab()

        navigate('http://www.eginstill.com/')
        location_to_open = Location(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        time.sleep(DEFAULT_FIREFOX_TIMEOUT)
        click(location_to_open)

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists,
                    'Content before scrolling using mouse wheel with preference equals 200 is on the page')
        click(scroll_content_pattern)

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_pattern, scroll, (-value, None), 100, DEFAULT_UI_DELAY)
        assert_true(self, after_scroll_content_exists,
                    'Scroll Down using mouse wheel is successful with mousewheel preference equals 200.')

        after_scroll_content_exists = \
            scroll_until_pattern_found(scroll_content_pattern, scroll, (value, None), 100, DEFAULT_UI_DELAY)
        assert_true(self, after_scroll_content_exists,
                    'Scroll Up using mouse wheel is successful with mousewheel preference equals 200.')


        # Mousewheel scrolling preference is 50
        change_preference('mousewheel.default.delta_multiplier_y', '50')

        same_value_exists = check_preference('mousewheel.default.delta_multiplier_y', '50')
        assert_true(self, same_value_exists, 'The value is changed to 50')
        close_tab()

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists,
                    'Content before scrolling using mouse wheel with preference equals 50 is on the page')
        click(scroll_content_pattern)

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_pattern, scroll, (-value*2, None), 100, DEFAULT_UI_DELAY)
        assert_true(self, after_scroll_content_exists,
                    'Scroll Down using mouse wheel is successful with mousewheel preference equals 50.')

        after_scroll_content_exists = \
            scroll_until_pattern_found(scroll_content_pattern, scroll, (value*2, None), 100, DEFAULT_UI_DELAY)
        assert_true(self, after_scroll_content_exists,
                    'Scroll Up using mouse wheel is successful with mousewheel preference equals 50.')

        # Set the default params to mousewheel
        change_preference('mousewheel.default.delta_multiplier_y', '100')
        same_value_exists = check_preference('mousewheel.default.delta_multiplier_y', '100')
        assert_true(self, same_value_exists, 'The value is changed to default value')


