# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Private Browsing session is lost after restarting Firefox'
        self.test_case_id = '107721'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        private_window_inactive_pattern = Pattern('private_window_inactive.png')
        browser_console_title_pattern = Pattern('browser_console_title.png')

        new_private_window()
        private_window_is_loaded = exists(PrivateWindow.private_window_pattern, 20)
        assert_true(self, private_window_is_loaded,
                    'Private windows is loaded.')

        open_browser_console()
        browser_console_opened = exists(browser_console_title_pattern, 20)
        assert_true(self, browser_console_opened,
                    'Browser Console is successfully opened. Browser Console is in focus. Restarting Firefox.')

        restart_via_console()
        wait_for_firefox_restart()

        try:
            private_mozilla_closed = wait_vanish(private_window_inactive_pattern, 20)
            assert_true(self, private_mozilla_closed,
                        'Firefox restarted. Private browsing session is not restored.')
        except FindError:
            raise FindError('Private browser windows was not closed.')

        browser_console_active = exists(browser_console_title_pattern, 40)
        assert_true(self, browser_console_active,
                    'Browser Console is active. Closing Browser Console.')

        close_tab()

        try:
            browser_console_closed = wait_vanish(browser_console_title_pattern, 20)
            assert_true(self, browser_console_closed,
                        'Browser console was closed successfully.')
        except FindError:
            raise FindError('Browser console was not closed.')
