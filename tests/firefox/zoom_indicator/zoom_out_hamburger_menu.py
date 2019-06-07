# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test case that checks the zoom out functionality from the hamburger menu.',
        locale=['en-US'],
        test_case_id='7456',
        test_suite_id='242',
    )
    def run(self, firefox):
        url1 = 'about:home'
        url2 = LocalWeb.FIREFOX_TEST_SITE
        search_bar_pattern = LocationBar.SEARCH_BAR
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        hamburger_menu_zoom_indicator_pattern = HamburgerMenu.HAMBURGER_MENU_ZOOM_INDICATOR
        zoom_control_toolbar_decrease_pattern = NavBar.ZOOM_OUT
        zoom_control_90_pattern = NavBar.ZOOM_RESET_BUTTON_90
        urlbar_zoom_button_90_pattern = LocationBar.URLBAR_ZOOM_BUTTON_90
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU

        navigate(url1)

        expected = exists(hamburger_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, hamburger menu found.'

        expected = exists(search_bar_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        navigate(url2)

        expected = exists(hamburger_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, hamburger menu found.'

        region = create_region_for_url_bar()

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        new_region = create_region_for_hamburger_menu()

        expected = exists(hamburger_menu_zoom_indicator_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'By default zoom indicator is 100% in hamburger menu.'

        click(zoom_control_toolbar_decrease_pattern)

        expected = exists(zoom_control_90_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'Zoom indicator is correctly displayed in hamburger menu after zoom level decrease.'

        click(hamburger_menu_pattern)

        new_reg = create_region_for_url_bar()

        expected = exists(urlbar_zoom_button_90_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_reg)
        assert expected, 'Zoom indicator is correctly displayed in the url bar after zoom level decrease.'
