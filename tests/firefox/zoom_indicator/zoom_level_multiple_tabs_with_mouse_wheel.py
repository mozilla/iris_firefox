# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case verifies the zoom level on multiple tabs using multiple sites and mouse wheel.',
        locale=['en-US', 'zh-CN', 'es-ES', 'de', 'fr', 'ru', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja'],
        test_case_id='7453',
        test_suite_id='242'
    )
    def run(self, firefox):
        url_1 = LocalWeb.FIREFOX_TEST_SITE
        url_2 = LocalWeb.FIREFOX_TEST_SITE_2
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110

        navigate(url_1)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        region = create_region_for_url_bar()

        click(hamburger_menu_pattern.target_offset(-170, 0))

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        zoom_with_mouse_wheel(1, ZoomType.IN)

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Zoom level successfully increased, zoom indicator found in the url bar.'

        new_tab()
        navigate(url_1)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Zoom indicator still displays 110% in the new tab opened for the site for which the zoom ' \
                         'level was set.'

        new_tab()
        navigate(url_2)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom indicator not displayed in the url bar.'
