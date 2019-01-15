# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.test_case_id = '105525'
        self.test_suite_id = '1956'
        self.meta = 'Firefox can be set to no longer accept cookies from visited websites.'
        self.locale = ['en-US']

    def run(self):
        block_all_cookies_pattern = Pattern('block_all_cookies.png')
        cookies_blocking_strictness_menu_pattern = Pattern('cookies_blocking_strictness_menu.png')
        cookies_ticked_pattern = Pattern('block_cookies_ticked.png')
        cookies_unticked_pattern = Pattern('block_cookies_unticked.png')
        cookies_window_title_pattern = Pattern('cookies_window_title.png')
        custom_content_blocking_pattern = Pattern('custom_content_blocking.png')
        manage_cookies_data_pattern = Pattern('manage_cookies_data.png')
        site_cookies_pattern = Pattern('site_cookies.png')
        youtube_logo_pattern = Pattern('youtube_logo.png')

        new_tab()
        navigate('about:preferences#privacy')
        preferences_opened = exists(custom_content_blocking_pattern)
        assert_true(self, preferences_opened, 'The page is successfully displayed.')

        click(custom_content_blocking_pattern)
        options_displayed = exists(cookies_unticked_pattern)
        assert_true(self, options_displayed, 'The options are properly displayed.')

        click(cookies_unticked_pattern)
        checkbox_set_successfully = exists(cookies_ticked_pattern)
        strictness_menu_appeared = exists(cookies_blocking_strictness_menu_pattern)
        assert_true(self, checkbox_set_successfully, 'The checkbox is successfully set.')
        assert_true(self, strictness_menu_appeared, 'Strictness menu appeared.')

        click(cookies_blocking_strictness_menu_pattern)
        dropdown_opened = exists(block_all_cookies_pattern)
        assert_true(self, dropdown_opened, 'Strictness dropdown menu opened')
        click(block_all_cookies_pattern)

        navigate('https://www.youtube.com/')
        site_loaded = exists(youtube_logo_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, site_loaded, 'The website is successfully displayed.')

        navigate('about:preferences#privacy')
        paste('manage data')
        cookies_data_button_located = exists(manage_cookies_data_pattern)
        assert_true(self, cookies_data_button_located, '\"Manage cookies data\" button displayed.')

        click(manage_cookies_data_pattern)
        cookies_window_opened = exists(cookies_window_title_pattern)
        assert_true(self, cookies_window_opened, 'Cookies window displayed.')

        paste('yout')
        site_cookies_not_saved = not exists(site_cookies_pattern)
        assert_true(self, site_cookies_not_saved, 'No cookies are saved from the YouTube website.')
