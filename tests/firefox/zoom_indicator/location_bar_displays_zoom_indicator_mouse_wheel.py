# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This test case verifies the presence of the zoom indicator in the location bar '
                    'using the mousewheel.',
        locale=['en-US', 'zh-CN', 'es-ES', 'de', 'fr', 'ru', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja'],
        test_case_id='7450',
        test_suite_id='242',
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110

        navigate(url)
        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, 'Page successfully opened, firefox logo found.'

        select_zoom_menu_option(Option.ZOOM_TEXT_ONLY)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        region = create_region_for_url_bar()
        click(LocalWeb.FIREFOX_LOGO)

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        zoom_with_mouse_wheel(1, ZoomType.IN)
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU

        new_region = create_region_for_url_bar()

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'Zoom level successfully increased, zoom indicator found in the url bar.'
