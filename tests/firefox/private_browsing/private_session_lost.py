# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Private Browsing session is lost after restarting Firefox',
        test_case_id='107721',
        test_suite_id='1826',
        locales=['en-US'],
    )
    def run(self, firefox):
        private_window_inactive_pattern = Pattern('private_window_inactive.png')
        browser_console_title_pattern = Pattern('browser_console_title.png')

        new_private_window()
        private_window_is_loaded = exists(PrivateWindow.private_window_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert private_window_is_loaded is True, 'Private windows is loaded.'

        open_browser_console()
        browser_console_opened = exists(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened is True, 'Browser Console is successfully opened. ' \
                                               'Browser Console is in focus. Restarting Firefox.'

        restart_via_console()

        try:
            private_mozilla_closed = wait_vanish(private_window_inactive_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert private_mozilla_closed is True, 'Firefox restarted. ' \
                                                   'Private browsing session is not restored.'
        except FindError:
            raise FindError('Private browser windows was not closed.')

        browser_console_active = exists(browser_console_title_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert browser_console_active is True, 'Browser Console is active. Closing Browser Console.'

        close_tab()

        try:
            browser_console_closed = wait_vanish(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert browser_console_closed is True, 'Browser console was closed successfully.'
        except FindError:
            raise FindError('Browser console was not closed.')
