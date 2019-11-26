# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This is a test case that resets the zoom level from the menu bar.",
        locale=["en-US"],
        test_case_id="7460",
        test_suite_id="242",
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Page successfully loaded, firefox logo found."

        select_location_bar()

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Zoom indicator not displayed by default in the url bar."

        select_zoom_menu_option(Option.ZOOM_IN)

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Zoom level successfully increased, zoom indicator found in the url bar."

        select_zoom_menu_option(Option.RESET)

        region = create_region_for_url_bar()
        expected = exists(
            url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT, region=region
        )
        assert expected, "Zoom indicator not displayed in the url bar after zoom level reset."
