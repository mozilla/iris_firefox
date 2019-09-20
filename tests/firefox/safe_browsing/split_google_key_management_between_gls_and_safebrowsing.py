# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1531176 - Split the Google key management between gls and safe browsing',
        test_case_id='294453',
        test_suite_id='69',
        locale=['en-US'],
    )
    def run(self, firefox):
        browser_console_title_pattern = Pattern('browser_console_title.png')
        console_log_arrow_icon_pattern = Pattern('console_log_arrow_icon.png')
        clear_console_icon_pattern = Pattern('clear_console_icon.png')

        change_preference('devtools.chrome.enabled', 'true')

        open_browser_console()

        browser_console_opened = exists(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser Console opened'

        clear_console_icon_displayed = exists(clear_console_icon_pattern)
        assert clear_console_icon_displayed, 'Clear console icon displayed'

        clear_console_icon_width, clear_console_icon_height = clear_console_icon_pattern.get_size()

        click(clear_console_icon_pattern)

        click(clear_console_icon_pattern.target_offset(clear_console_icon_width * 5, 0), 1)

        type('logs')

        click(clear_console_icon_pattern.target_offset(clear_console_icon_width * 5, clear_console_icon_height * 10), 1)

        paste('print(AppConstants.MOZ_GOOGLE_SAFEBROWSING_API_KEY)')

        type(Key.ENTER)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        value_returned = exists(console_log_arrow_icon_pattern)
        assert value_returned, 'value_returned'

        right_click(console_log_arrow_icon_pattern)
        type('c')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        returned_value = get_clipboard().replace('\n', '').replace('\r', '').replace('\"', '')
        assert returned_value.endswith('c5Dovo'), 'The returned value ends in: c5Dovo'

        click(clear_console_icon_pattern)

        click(clear_console_icon_pattern.target_offset(clear_console_icon_width * 5, clear_console_icon_height * 10), 1)

        paste('print(AppConstants.MOZ_GOOGLE_LOCATION_SERVICE_API_KEY)')

        type(Key.ENTER)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        value_returned = exists(console_log_arrow_icon_pattern)
        assert value_returned, 'value_returned'

        right_click(console_log_arrow_icon_pattern)
        type('c')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        returned_value = get_clipboard().replace('\n', '').replace('\r', '').replace('\"', '')
        assert returned_value.endswith('_rptiQ'), 'The returned value ends in: _rptiQ'

        close_window_control('auxiliary')
