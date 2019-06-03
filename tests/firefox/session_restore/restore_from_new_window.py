# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Session restore can be performed from a new window',
        test_case_id='C117040',
        test_suite_id='68',
        locales=Locales.ENGLISH,
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert website_one_loaded, 'Page 1 successfully loaded, firefox logo found.'

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        website_two_loaded = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert website_two_loaded, 'Page 2 successfully loaded, mozilla logo found.'

        firefox.restart()

        click_hamburger_menu_option('Restore Previous Session')

        select_tab("5")
        website_one_loaded = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert website_one_loaded, 'Page 1 successfully restored from previous session.'

        select_tab("4")
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert website_two_loaded, 'Page 2 successfully restored from previous session.'
