# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Previously closed tabs can be restored by using keyboard combinations',
        test_case_id='117047',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        local_url = [LocalWeb.FIREFOX_TEST_SITE, LocalWeb.FIREFOX_TEST_SITE_2, LocalWeb.FOCUS_TEST_SITE,
                     LocalWeb.FOCUS_TEST_SITE_2, LocalWeb.MOZILLA_TEST_SITE]
        local_url_logo_pattern = [LocalWeb.FIREFOX_LOGO, LocalWeb.FIREFOX_LOGO, LocalWeb.FOCUS_LOGO,
                                  LocalWeb.FOCUS_LOGO, LocalWeb.MOZILLA_LOGO]

        for _ in range(5):
            new_tab()
            navigate(local_url[_])
            website_loaded = exists(local_url_logo_pattern[_], FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert website_loaded, f'Website {_ + 1} loaded'

        [close_tab() for _ in range(4)]

        one_tab_exists = exists(local_url_logo_pattern[0], FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert one_tab_exists, f'One opened tab left. {len(local_url) - 1} tabs were successfully closed.'

        for _ in range(4):
            undo_close_tab()
            tab_is_restored = exists(local_url_logo_pattern[_ + 1])  # +1 as url[0] is one opened tab
            assert tab_is_restored, f'Tab {_ + 2} successfully restored'
