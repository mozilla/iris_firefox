# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description=' The total usage of cookies, site data and cache is successfully displayed ',
        test_case_id='143618',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        stored_cookies_cache_pattern = Pattern('stored_cookies_cache.png')
        zero_bytes_cache_pattern = Pattern('zero_bytes_cache.png')
        ui_timeout = 1
        quick_click_duration = 0.3
        scroll_length = -Screen.SCREEN_HEIGHT // 5
        if not OSHelper.is_windows():
            scroll_length = -5

        navigate('about:preferences#privacy')

        prefs_opened = exists(AboutPreferences.Privacy.TRACKING_PROTECTION_EXCEPTIONS_BUTTON)
        assert prefs_opened, 'Preferences are opened'

        exceptions_button_location = find(AboutPreferences.Privacy.TRACKING_PROTECTION_EXCEPTIONS_BUTTON)

        click(exceptions_button_location.above(Screen.SCREEN_HEIGHT // 10), quick_click_duration)

        cookies_site_data_reached = scroll_until_pattern_found(stored_cookies_cache_pattern, scroll, (scroll_length,),
                                                               timeout=ui_timeout)
        assert cookies_site_data_reached, '"Cookies and Site Data" block is reached'

        some_memory_is_used = not exists(zero_bytes_cache_pattern.similar(0.9), ui_timeout)
        assert some_memory_is_used, 'The amount is different from 0 MB'
