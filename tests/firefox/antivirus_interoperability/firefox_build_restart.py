# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox Build Restart.',
        locale=['en-US'],
        test_case_id='217866',
        test_suite_id='3063'
    )
    def run(self, firefox):
        browser_console_opened_pattern = Pattern('browser_console_opened.png')

        open_browser_console()
        assert exists(browser_console_opened_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), 'Browser console is opened.'

        click(browser_console_opened_pattern)
        restart_via_console()
        assert exists(browser_console_opened_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), 'Firefox is restarted.'

        close_window_control('auxiliary')
        restore_firefox_focus()
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        assert exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'The page is properly loaded. No crashes occur.'
