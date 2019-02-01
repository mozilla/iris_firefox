# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Test case: No crash or bluescreen after closing a tab while in private browsing mode.'
        self.test_case_id = '219584'
        self.test_suite_id = '3063'
        self.locale = ['en-US']

    def run(self):
        click_hamburger_menu_option('New Private Window')
        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert_true(self, private_window_opened, 'Private window opened.')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Webpage is opened in tab')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        mozilla_test_site_opened = exists(LocalWeb.MOZILLA_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, mozilla_test_site_opened, 'Webpage opened in second tab')

        close_tab()
        tab_closed = not exists(LocalWeb.MOZILLA_LOGO)
        assert_true(self, tab_closed, 'Tab is closed successfully')

        other_tab_displayed = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert_true(self, other_tab_displayed, 'First tab displayed, no "BSOD" occurred')

        close_window()
