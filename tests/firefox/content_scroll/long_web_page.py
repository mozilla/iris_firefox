# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Scrolling works properly on long web pages.',
        test_case_id='4660',
        test_suite_id='102',
        locale=['en-US'],
    )
    def run(self, firefox):
        scroll_content_pattern = Pattern('about_us_content.png')
        scroll_content_after_zoomed_in_pattern = Pattern('after_zoomed_in_content.png')
        after_scroll_content_pattern = Pattern('after_scroll_content.png')

        if OSHelper.is_windows():
            value = Screen.SCREEN_HEIGHT
        elif OSHelper.is_mac():
            value = 200
        else:
            value = 10

        navigate('http://www.eginstill.com/')

        location_to_open = Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2)
        time.sleep(FirefoxSettings.FIREFOX_TIMEOUT)

        Mouse().general_click(location_to_open)

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert before_scroll_content_exists is True, 'The page content is loaded'

        click(scroll_content_pattern)

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_pattern, Mouse().scroll, (0, -value), 100,
                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert after_scroll_content_exists is True, 'Scroll down using mouse wheel on the long web page is successful'

        [zoom_in() for _ in range(2)]

        after_scroll_content_exists = \
            scroll_until_pattern_found(scroll_content_after_zoomed_in_pattern, Mouse().scroll, (0, value), 100,
                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert after_scroll_content_exists is True, 'Scroll up using mouse wheel after zooming is successful'
