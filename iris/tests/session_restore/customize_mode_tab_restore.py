
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1364483 - Customize Mode tab doesn\'t get restored anymore'
        self.test_case_id = '116004'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        customize_option_pattern = Pattern('customize_option.png')
        browser_console_pattern = Pattern('browser_console_opened.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, SCREEN_WIDTH, home_height * 4)

        click_hamburger_menu_option('Customize...')

        customize_page_opened = exists(customize_option_pattern, Settings.FIREFOX_TIMEOUT, tabs_region)
        assert_true(self, customize_page_opened, '"Customize..." mode is properly open.')

        open_browser_console()

        for _ in range(3):
            open_browser_console()
            browser_console_opened = exists(browser_console_pattern, Settings.FIREFOX_TIMEOUT)
            if browser_console_opened:
                break

        assert_true(self, browser_console_opened, 'Browser console displayed')

        restart_via_console()

        browser_console_reopened = exists(browser_console_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, browser_console_reopened, 'Browser console reopened')

        click(browser_console_pattern)

        close_window_control('auxiliary')

        customize_page_opened = exists(customize_option_pattern, Settings.FIREFOX_TIMEOUT, tabs_region)
        assert_true(self, customize_page_opened, 'Firefox is restarted and "Customize..." mode is properly restored.')
