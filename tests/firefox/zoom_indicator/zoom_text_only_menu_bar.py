# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks that \'zoom text only\' option works correctly.',
        locale=['en-US'],
        test_case_id='7461',
        test_suite_id='242',
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110
        urlbar_zoom_button_90_pattern = LocationBar.URLBAR_ZOOM_BUTTON_90
        zoom_text_only_check_pattern = Pattern('zoom_text_only_check.png')

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        select_zoom_menu_option(Option.ZOOM_TEXT_ONLY)

        open_zoom_menu()

        expected = exists(zoom_text_only_check_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, '\'Zoom text only\' option successfully checked.'

        close_find()
        close_find()

        select_location_bar()

        expected = exists(url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Zoom indicator not displayed in the url bar after \'zoom text only\' option is set.'

        zoom_in()

        region = create_region_for_url_bar()

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom level successfully increased, zoom indicator found in the url bar.'

        zoom_out()
        zoom_out()

        expected = exists(urlbar_zoom_button_90_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom level successfully decreased, zoom indicator found in the url bar.'

        select_zoom_menu_option(Option.RESET)

        new_region = create_region_for_url_bar()

        expected = exists(url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT, new_region)
        assert expected, 'Zoom indicator not displayed in the url bar after zoom level is reset.'

        open_zoom_menu()

        expected = exists(zoom_text_only_check_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, '\'Zoom text only\' option is still checked.'

        close_find()
        close_find()
