# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox can be set to no longer accept third-party cookies.'
        self.test_case_id = '106156'
        self.test_suite_id = '1826'
        self.locale = ['en-US']

    def run(self):
        block_all_third_party_cookies_pattern = Pattern('block_all_third_party_cookies.png')
        clear_data_button_pattern = Pattern('clear_button.png')
        confirm_clear_data_pattern = Pattern('confirm_clear_data.png')
        cookies_blocking_strictness_menu_pattern = Pattern('cookies_blocking_strictness_menu.png')
        cookies_list_empty_pattern = Pattern('cookies_list_empty.png')
        cookies_blocking_ticked_pattern = Pattern('block_cookies_ticked.png').similar(0.9)
        cookies_blocking_unticked_pattern = Pattern('block_cookies_unticked.png').similar(0.9)
        cookies_window_title_pattern = Pattern('cookies_window_title.png')
        custom_content_blocking_unticked_pattern = Pattern('custom_content_blocking_unticked.png')
        custom_content_blocking_ticked_pattern = Pattern('custom_content_blocking_ticked.png')
        manage_cookies_data_pattern = Pattern('manage_cookies_data.png')
        open_clear_data_window_pattern = Pattern('open_clear_data_window.png')
        site_cookie_one_pattern = Pattern('site_cookie_one.png')
        site_cookie_two_pattern = Pattern('site_cookie_two.png')
        site_tab_pattern = Pattern('prosport_tab.png')

        navigate('about:preferences#privacy')
        preferences_opened = exists(custom_content_blocking_unticked_pattern)
        assert_true(self, preferences_opened, 'The privacy preferences page is successfully displayed.')

        click(custom_content_blocking_unticked_pattern)

        cookies_blocking_unticked = exists(cookies_blocking_unticked_pattern)

        if cookies_blocking_unticked:
            click(cookies_blocking_unticked_pattern)

        cookies_blocking_ticked = exists(cookies_blocking_ticked_pattern)
        assert_true(self, cookies_blocking_ticked, 'The "Cookies and Site Data" options are properly displayed.')

        strictness_menu_appeared = exists(cookies_blocking_strictness_menu_pattern)
        assert_true(self, strictness_menu_appeared, 'Cookies blocking strictness menu appear.')

        click(cookies_blocking_strictness_menu_pattern)

        strictness_dropdown_displayed = exists(block_all_third_party_cookies_pattern)
        assert_true(self, strictness_dropdown_displayed, 'Block all third party cookies blocking '
                                                         'dropdown menu displayed.')

        click(block_all_third_party_cookies_pattern)

        reload_page()

        preferences_opened = exists(custom_content_blocking_ticked_pattern)
        assert_true(self, preferences_opened, 'The privacy preferences page is successfully displayed.')

        paste('clear data')

        open_clear_data_button_displayed = exists(open_clear_data_window_pattern)
        assert_true(self, open_clear_data_button_displayed, '"Clear data" button displayed.')

        click(open_clear_data_window_pattern)

        clear_data_window_displayed = exists(clear_data_button_pattern)
        assert_true(self, clear_data_window_displayed, 'Clear data window displayed.')

        click(clear_data_button_pattern)

        message_window_displayed = exists(confirm_clear_data_pattern)
        assert_true(self, message_window_displayed, '"Clear data" message window displayed.')

        click(confirm_clear_data_pattern)

        navigate('https://www.prosport.ro/')
        site_loaded = exists(site_tab_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT * 2)
        assert_true(self, site_loaded, 'The "Prosport" website is successfully displayed.')

        navigate('about:preferences#privacy')
        preferences_opened = exists(custom_content_blocking_ticked_pattern)
        assert_true(self, preferences_opened, 'The page is successfully displayed.')

        paste('manage data')
        cookies_data_button_located = exists(manage_cookies_data_pattern)
        assert_true(self, cookies_data_button_located, '"Manage Data..." button displayed.')

        click(manage_cookies_data_pattern)

        cookies_data_window_opened = exists(cookies_window_title_pattern)
        assert_true(self, cookies_data_window_opened, 'Cookies data window opened.')

        site_cookie_one_saved = exists(site_cookie_one_pattern)
        assert_true(self, site_cookie_one_saved, 'Target site cookie saved.')

        site_cookie_two_saved = exists(site_cookie_two_pattern)
        assert_true(self, site_cookie_two_saved, 'Other target cookie saved.')

        click(site_cookie_one_pattern)

        type(Key.DELETE)  # There are two cookies must be left after visiting prosport.ro
        type(Key.DELETE)  # So it's needed to press "Delete" key twice to remove this site's cookies from list

        cookies_list_is_empty = exists(cookies_list_empty_pattern)
        assert_true(self, cookies_list_is_empty, 'No third-party cookies are saved')
