# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Previous Session can be restored from the Firefox menu',
        test_case_id='114837',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Mozilla test website is opened'

        new_tab()

        navigate(LocalWeb.POCKET_TEST_SITE)

        test_site_opened = exists(LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Pocket test website is opened'

        if OSHelper.is_mac():
            quit_firefox()
        elif OSHelper.is_linux():
            click_hamburger_menu_option('Quit')
        else:
            click_hamburger_menu_option('Exit')

        firefox.restart()

        firefox_restarted = exists(LocalWeb.IRIS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_restarted, 'Firefox restarted successfully'

        click_hamburger_menu_option('Restore')

        next_tab()

        first_tab_restored = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert first_tab_restored, 'Mozilla test website is restored'

        next_tab()

        second_tab_restored = exists(LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert second_tab_restored, 'Pocket test website is restored'

        all_tab_restored = first_tab_restored and second_tab_restored
        assert all_tab_restored, \
            'The previous session is successfully restored (All previously closed tabs are successfully restored).'
