# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "This is a test case that checks that Browser Control Console work as expected."
        self.test_case_id = '120464'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):

        url = "about:blank"
        browser_console = Pattern('browser_console.png')
        clear_web_console = Pattern('clear.png')

        navigate(url)
        pop_up_region = click_hamburger_menu_option('Web Developer')
        time.sleep(Settings.UI_DELAY_LONG)

        pop_up_region.click('Browser Console')
        time.sleep(Settings.UI_DELAY_LONG)
        expected_1 = exists(browser_console, 10)
        assert_true(self, expected_1, 'Browser Console successfully displayed.')

        # Check if the Browser Console options are available.
        expected_2 = exists(clear_web_console, 10)
        assert_true(self, expected_2, 'Clear the web console option is present.')

        click_window_control('close')
        try:
            expected_3 = wait_vanish(browser_console, 10)
            assert_true(self, expected_3, 'Browser Console successfully closed.')
        except FindError:
            logger.error('Browser Console not closed')

        # Access Browser Console by keyboard shortcut.
        open_browser_console()
        click_window_control("minimize")
        try:
            expected_4 = wait_vanish(browser_console, 10)
            assert_true(self, expected_4, 'Browser Console successfully minimized.')
        except FindError:
            logger.error('Browser Console not minimized.')

        restore_window_from_taskbar(option='browser_console')
        click_window_control("maximize")
        top_page = Region(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 4)
        try:
            mouse_move(clear_web_console)
            expected_5 = top_page.exists(browser_console, 10)
            assert_true(self, expected_5, 'Browser Console successfully maximized.')
        except FindError:
            logger.error('Browser Console not maximized.')

        click_window_control("close")
