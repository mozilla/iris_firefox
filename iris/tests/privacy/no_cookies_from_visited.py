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
        custom_content_blocking_unticked_pattern = Pattern('custom_content_blocking_unticked.png')
        custom_content_blocking_ticked_patten = Pattern('custom_content_blocking_ticked.png')
        manage_cookies_data_pattern = Pattern('manage_cookies_data.png')
        site_cookies_pattern = Pattern('site_cookies.png')
        youtube_logo_pattern = Pattern('youtube_logo.png')

        navigate('about:preferences#privacy')

        preferences_opened = exists(custom_content_blocking_unticked_pattern)
        assert_true(self, preferences_opened, 'The "about:preferences#privacy" page is successfully displayed.')

        click(custom_content_blocking_unticked_pattern)
        options_displayed = exists(cookies_unticked_pattern)
        assert_true(self, options_displayed,
                    'The cookies options are properly displayed at "Cookies and Site Data" section')
        click(cookies_unticked_pattern)

        checkbox_set_successfully = exists(cookies_ticked_pattern)
        assert_true(self, checkbox_set_successfully, 'The "Block cookies and site data" checkbox is successfully set.')

        strictness_menu_appeared = exists(cookies_blocking_strictness_menu_pattern)
        assert_true(self, strictness_menu_appeared, 'Strictness menu appeared.')

        click(cookies_blocking_strictness_menu_pattern)
        dropdown_opened = exists(block_all_cookies_pattern)
        assert_true(self, dropdown_opened, 'Strictness dropdown menu opened')

        click(block_all_cookies_pattern)

        navigate('https://www.youtube.com/')
        site_loaded = exists(youtube_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, site_loaded, 'The website is successfully displayed.')

        navigate('about:preferences#privacy')
        preferences_opened = exists(custom_content_blocking_ticked_patten, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, preferences_opened, 'The "about:preferences#privacy" page is successfully displayed.')

        paste('manage data')
        cookies_data_button_located = exists(manage_cookies_data_pattern)
        assert_true(self, cookies_data_button_located, '\"Manage cookies data\" button displayed.')

        click(manage_cookies_data_pattern)
        cookies_window_opened = exists(cookies_window_title_pattern)
        assert_true(self, cookies_window_opened, 'Cookies window displayed.')

        paste('yout')
        site_cookies_not_saved = not exists(site_cookies_pattern)
        assert_true(self, site_cookies_not_saved, 'No cookies are saved from the YouTube website.')
