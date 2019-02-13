# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Firefox Bulid Restart"
        self.test_case_id = "217866"
        self.test_suite_id = "3063"
        self.locale = ["en-US"]

    def run(self):
        browser_console_opened_pattern = Pattern('browser_console_opened.png')

        open_browser_console()

        browser_console_opened = exists(browser_console_opened_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, browser_console_opened, 'Browser console is opened')

        click(browser_console_opened_pattern)

        restart_via_console()

        firefox_is_restarted = exists(browser_console_opened_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_is_restarted, 'Firefox is restarted')

        close_window_control('auxiliary')

        restore_firefox_focus()

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'The page is properly loaded. No crashes occur')
