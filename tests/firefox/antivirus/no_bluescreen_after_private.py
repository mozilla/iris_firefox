# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Test case: No crash or bluescreen after closing a tab while in private browsing mode.',
        locale=['en-US'],
        test_case_id='219584',
        test_suite_id='3063'
    )
    def run(self, firefox):
        new_private_window()

        # time.sleep added to prevent navigation not in private window on low performance machines

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert private_window_opened, 'Private window opened.'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.DEFAULT_SITE_LOAD_TIMEOUT)
        assert soap_wiki_opened, 'Webpage is opened in tab'

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_test_site_opened = exists(LocalWeb.MOZILLA_LOGO, Settings.DEFAULT_SITE_LOAD_TIMEOUT)
        assert mozilla_test_site_opened, 'Webpage opened in second tab'

        close_tab()

        tab_closed = not exists(LocalWeb.MOZILLA_LOGO)
        assert tab_closed, 'Tab is closed successfully'

        other_tab_displayed = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert other_tab_displayed, 'First tab displayed, no "BSOD" occurred'

        close_window()
