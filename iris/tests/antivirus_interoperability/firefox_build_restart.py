# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Firefox Bulid Restart"
        self.test_case_id = "217866"
        self.test_suite_id = "3036"
        self.locale = ["en-US"]

    def run(self):
        web_console_button_pattern = Pattern('browser_console_button.png')
        web_developer_menu = Pattern('web_developer_menu.png')
        browser_console_opened_pattern = Pattern('browser_console_opened.png')

        click(NavBar.HAMBURGER_MENU)
        time.sleep(DEFAULT_UI_DELAY)
        click(web_developer_menu)
        time.sleep(DEFAULT_UI_DELAY)
        click(web_console_button_pattern)

        browser_console_opened = exists(browser_console_opened_pattern)
        assert_true(self, browser_console_opened, 'Browser console is opened')

        click(browser_console_opened_pattern)

        restart_via_console()

        firefox_is_restarted = exists(browser_console_opened_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_is_restarted, 'Firefox is restarted')

        restore_firefox_focus()

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert_true(self, soap_wiki_opened, 'The page is properly loaded. No crashes occur')
