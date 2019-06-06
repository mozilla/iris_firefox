# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test case that checks the zoom indicator in a private window when applying the Firefox' \
                    ' Menu Zoom Controls.',
        locale=['en-US'],
        test_case_id='7463',
        test_suite_id='242',
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_90_pattern = LocationBar.URLBAR_ZOOM_BUTTON_90
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110
        zoom_control_toolbar_increase_pattern = NavBar.ZOOM_IN
        zoom_control_toolbar_decrease_pattern = NavBar.ZOOM_OUT
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU

        new_private_window()
        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        region = create_region_for_url_bar()

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        new_region = create_region_for_hamburger_menu()

        expected = exists('100%', FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'By default zoom indicator is 100% in hamburger menu.'

        click(zoom_control_toolbar_increase_pattern)

        new_reg = create_region_for_url_bar()

        expected = exists('110%', FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'Zoom level successfully increased in hamburger menu.'

        click(hamburger_menu_pattern)

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_reg)
        assert expected, 'Zoom level successfully increased, zoom indicator displayed in the url bar.'

        click(hamburger_menu_pattern)

        click(zoom_control_toolbar_decrease_pattern, 1)
        click(zoom_control_toolbar_decrease_pattern, 1)

        restore_firefox_focus()

        new_region_90 = create_region_for_hamburger_menu()

        expected = exists('90%', FirefoxSettings.FIREFOX_TIMEOUT, region=new_region_90)
        assert expected, 'Zoom level successfully decreased in hamburger menu.'

        click(hamburger_menu_pattern)

        expected = exists(urlbar_zoom_button_90_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_reg)
        assert expected, 'Zoom level successfully decreased, zoom indicator displayed in the url bar.'
