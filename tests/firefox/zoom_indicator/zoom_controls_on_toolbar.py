# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test case that checks the zoom controls on toolbar.',
        locale=['en-US'],
        test_case_id='7443',
        test_suite_id='242',
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        zoom_controls_customize_page_pattern = NavBar.ZOOM_CONTROLS_CUSTOMIZE_PAGE
        default_zoom_level_toolbar_customize_page_pattern = NavBar.DEFAULT_ZOOM_LEVEL_TOOLBAR_CUSTOMIZE_PAGE
        zoom_reset_button_100_pattern = NavBar.ZOOM_RESET_BUTTON
        zoom_control_toolbar_decrease_pattern = NavBar.ZOOM_OUT
        zoom_control_toolbar_increase_pattern = NavBar.ZOOM_IN
        zoom_control_90_pattern = NavBar.ZOOM_RESET_BUTTON_90
        zoom_control_110_pattern = NavBar.ZOOM_RESET_BUTTON_110
        toolbar_pattern = NavBar.TOOLBAR

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        region = create_region_for_url_bar()

        expected = exists(url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        click_hamburger_menu_option('Customize...')

        expected = exists(zoom_controls_customize_page_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Zoom controls found in the \'Customize\' page.'

        drag_drop(zoom_controls_customize_page_pattern, toolbar_pattern, duration=1)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        reset_mouse()

        expected = exists(default_zoom_level_toolbar_customize_page_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=Region(0, 0, Screen.SCREEN_WIDTH, 300))
        assert expected, 'Zoom controls successfully dragged and dropped in toolbar.'

        close_customize_page()

        new_region = create_region_for_url_bar()

        expected = exists(zoom_reset_button_100_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'Zoom controls still displayed in toolbar after the Customize page is closed.'

        expected = exists(url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT,
                          region=new_region)
        assert expected, 'Zoom indicator not displayed in the url bar for default zoom level.'

        click(zoom_control_toolbar_decrease_pattern)

        expected = exists(zoom_control_90_pattern.similar(0.4), FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'Zoom controls are correctly displayed in toolbar after zoom level is decreased.'

        click(zoom_control_toolbar_increase_pattern)

        expected = exists(zoom_reset_button_100_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'Zoom controls are correctly displayed in toolbar after zoom level is increased.'

        click(zoom_control_toolbar_increase_pattern)

        expected = exists(zoom_control_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'Zoom controls are correctly displayed in toolbar after the second zoom level increase.'

        expected = exists(url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT,
                          region=new_region)
        assert expected, 'Zoom indicator not displayed in the url bar after zoom control is activated in toolbar.'

        # Decrease the zoom indicator to 100% so that it won't be displayed in the url bar after zoom controls
        # deactivation.
        click(zoom_control_toolbar_decrease_pattern)

        new_region_zoom_remove = create_region_for_url_bar()

        expected = exists(zoom_reset_button_100_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region_zoom_remove)
        assert expected, 'Zoom controls are correctly displayed in toolbar after several zoom level ' \
                         'increases/decreases.'

        restore_firefox_focus()

        remove_zoom_indicator_from_toolbar()

        expected = exists(url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT,
                          region=new_region)
        assert expected, 'Zoom indicator not displayed in the url bar after zoom control is removed from toolbar.'

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        new_reg = create_region_for_hamburger_menu()

        expected = exists('100%', FirefoxSettings.FIREFOX_TIMEOUT, region=new_reg)
        assert expected, 'By default zoom level is 100% in hamburger menu.'
