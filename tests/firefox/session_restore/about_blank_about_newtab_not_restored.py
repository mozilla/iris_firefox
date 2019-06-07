# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1323987 - about:blank and about:newtab aren\'t restored by Session Restore',
        test_case_id='116003',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        blank_white_squre_400_200_pattern = Pattern('blank_white_squre_400_200.png')
        middle_vertical_region = Screen.MIDDLE_THIRD_VERTICAL
        center_region = middle_vertical_region.middle_third_horizontal()

        navigate('about:newtab')
        top_sites_available = exists(Utils.TOP_SITES, Settings.FIREFOX_TIMEOUT)
        assert top_sites_available, 'about:newtab website loaded successfully'

        new_tab()
        navigate('about:blank')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)  # Pattern of new tab will be found before loading about:blank

        about_blank_tab = exists(blank_white_squre_400_200_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT, center_region)
        assert about_blank_tab, 'about:blank website loaded successfully'

        firefox.restart(image=LocalWeb.IRIS_LOGO_ACTIVE_TAB)

        click_hamburger_menu_option('Restore Previous Session')

        close_tab()

        top_sites_available = exists(Utils.TOP_SITES, FirefoxSettings.TINY_FIREFOX_TIMEOUT, Screen.LEFT_HALF)
        assert top_sites_available, 'about:newtab website restored successfully'

        next_tab()

        about_blank_tab = exists(blank_white_squre_400_200_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT, center_region)
        assert about_blank_tab, 'about:blank website restored successfully'
