# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test case that checks the zoom level reset functionality from the hamburger menu.',
        locale=['en-US'],
        test_case_id='7457',
        test_suite_id='242',
    )
    def run(self, firefox):
        url1 = 'about:home'
        url2 = LocalWeb.FIREFOX_TEST_SITE
        search_bar_pattern = LocationBar.SEARCH_BAR
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        hamburger_menu_zoom_indicator_pattern = HamburgerMenu.HAMBURGER_MENU_ZOOM_INDICATOR
        zoom_control_toolbar_increase_pattern = NavBar.ZOOM_IN
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU

        navigate(url1)

        expected = exists(hamburger_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, hamburger menu found.'

        expected = exists(search_bar_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        if OSHelper.is_windows():  # fix issue when on hover on navbar image is not being recognized
            search_bar_hover_pattern = Pattern("search_bar_hover.png")
            expected = expected or exists(search_bar_hover_pattern, FirefoxSettings.FIREFOX_TIMEOUT)

        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        navigate(url2)

        expected = exists(hamburger_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, hamburger menu found.'

        region = create_region_for_url_bar()

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        new_region = create_region_for_hamburger_menu()

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        expected = exists(hamburger_menu_zoom_indicator_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'By default zoom indicator is 100% in hamburger menu.'

        zoom_increase_button = exists(zoom_control_toolbar_increase_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert zoom_increase_button, 'zoom_control_toolbar_increase_pattern'

        click(zoom_control_toolbar_increase_pattern, 1)

        restore_firefox_focus()

        new_region_110 = create_region_for_hamburger_menu()

        expected = exists('110%', FirefoxSettings.FIREFOX_TIMEOUT, region=new_region_110)
        assert expected, 'Zoom indicator is correctly displayed in hamburger menu after zoom level is increased.'

        click(hamburger_menu_pattern)

        new_reg = create_region_for_url_bar()

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_reg)
        assert expected, 'Zoom indicator is correctly displayed in the url bar after zoom level is increased.'

        new_region_default = create_region_for_hamburger_menu()

        click(NavBar.ZOOM_OUT)

        select_location_bar()

        expected = exists(hamburger_menu_zoom_indicator_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=new_region_default)
        assert expected, 'Zoom indicator is successfully reset to default in hamburger menu.'

        reg_url = create_region_for_url_bar()

        if OSHelper.is_windows() or OSHelper.is_linux():
            expected = exists(url_bar_default_zoom_level_pattern.similar(0.95), FirefoxSettings.FIREFOX_TIMEOUT,
                              region=reg_url)
            assert expected, 'Zoom indicator is displayed anymore in the url bar.'
        else:
            expected = exists(url_bar_default_zoom_level_pattern.similar(0.93), FirefoxSettings.FIREFOX_TIMEOUT,
                              region=reg_url)
            assert expected, 'Zoom indicator is displayed anymore in the url bar.'
