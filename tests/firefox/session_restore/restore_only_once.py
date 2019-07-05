# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to restore a session only once',
        test_case_id='115423',
        test_suite_id='68',
        locales=Locales.ENGLISH,
    )
    def run(self, firefox):
        url_first = LocalWeb.FIREFOX_TEST_SITE
        url_second = LocalWeb.FIREFOX_TEST_SITE_2

        change_preference('browser.sessionstore.resume_session_once', 'true')

        new_tab()
        navigate(url_first)
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert website_one_loaded, 'Page 1 successfully loaded, firefox logo found.'

        new_tab()
        navigate(url_second)
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert website_two_loaded, 'Page 2 successfully loaded, firefox logo found.'

        firefox.restart()

        previous_tab()
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert website_one_loaded, 'Page 1 successfully loaded after restart.'

        previous_tab()
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert website_two_loaded, 'Page 2 successfully loaded after restart.'

        firefox.restart()

        previous_tab()
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO)
        assert website_one_loaded is False, 'Page 1 was not loaded after second restart.'

        previous_tab()
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO)
        assert website_two_loaded is False, 'Page 2 was not loaded after second restart.'
