# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Scrolling with different settings at browser-level.',
        test_case_id='4714',
        test_suite_id='102',
        locale=['en-US']
    )
    def run(self, firefox):
        scroll_content_pattern = Pattern('about_us_content.png')
        after_scroll_content_pattern = Pattern('after_scroll_content.png')

        if OSHelper.is_windows():
            value = Screen.SCREEN_HEIGHT/2
        elif OSHelper.is_linux():
            value = 5
        else:
            value = 100

        # Mousewheel scrolling preference is 200
        change_preference('mousewheel.default.delta_multiplier_y', '200')

        same_value_exists = check_preference('mousewheel.default.delta_multiplier_y', '200')
        assert same_value_exists is True, 'The value is changed to 200'

        close_tab()

        navigate('http://www.eginstill.com/')

        location_to_open = Location(Screen.SCREEN_WIDTH/2, Screen.SCREEN_HEIGHT/2)
        time.sleep(FirefoxSettings.FIREFOX_TIMEOUT)

        click(location_to_open)

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using mouse wheel ' \
                                                     'with preference equals 200 is on the page'
        click(scroll_content_pattern)

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_pattern, Mouse().scroll, (None, -value), 100,
                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert after_scroll_content_exists is True, 'Scroll Down using mouse wheel is successful' \
                                                    ' with mousewheel preference equals 200.'

        after_scroll_content_exists = \
            scroll_until_pattern_found(scroll_content_pattern, Mouse().scroll, (None, value), 100,
                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert after_scroll_content_exists is True, 'Scroll Up using mouse wheel is successful' \
                                                    'with mousewheel preference equals 200.'

        # Mousewheel scrolling preference is 50
        change_preference('mousewheel.default.delta_multiplier_y', '50')

        same_value_exists = check_preference('mousewheel.default.delta_multiplier_y', '50')
        assert same_value_exists is True, 'The value is changed to 50'

        close_tab()

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using mouse wheel' \
                                                     ' with preference equals 50 is on the page'
        click(scroll_content_pattern)

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_pattern, Mouse().scroll, (None, -value*2), 100,
                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert after_scroll_content_exists is True, 'Scroll Down using mouse wheel is successful' \
                                                    ' with mousewheel preference equals 50.'

        after_scroll_content_exists = \
            scroll_until_pattern_found(scroll_content_pattern, Mouse().scroll, (None, value*2), 100,
                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert after_scroll_content_exists is True, 'Scroll Up using mouse wheel is successful' \
                                                    ' with mousewheel preference equals 50.'

        # Set the default params to mousewheel
        change_preference('mousewheel.default.delta_multiplier_y', '100')

        same_value_exists = check_preference('mousewheel.default.delta_multiplier_y', '100')
        assert same_value_exists is True, 'The value is changed to default value'
