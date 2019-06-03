# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1364483 - Customize Mode tab doesn\'t get restored anymore',
        test_case_id='116004',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        browser_console_pattern = Pattern('browser_console_opened.png')
        customize_option_pattern = Pattern('customize_option.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Rectangle(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

        click_hamburger_menu_option('Customize...')

        customize_page_opened = exists(customize_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT, tabs_region)
        assert customize_page_opened, '"Customize..." mode is properly open.'

        open_browser_console()

        for _ in range(3):
            open_browser_console()
            browser_console_opened = exists(browser_console_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            if browser_console_opened:
                break

        assert browser_console_opened, 'Browser console displayed'

        restart_via_console()

        browser_console_reopened = exists(browser_console_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert browser_console_reopened, 'Browser console reopened'

        click(browser_console_pattern)

        close_window_control('auxiliary')

        customize_page_opened = exists(customize_option_pattern, Settings.FIREFOX_TIMEOUT, tabs_region)
        assert customize_page_opened, 'Firefox is restarted and "Customize..." mode is properly restored.'
