# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case checks the zoom indicator animation from the url bar.",
        locale=["en-US", "zh-CN", "es-ES", "de", "fr", "ru", "ko", "pt-PT", "vi", "pl", "tr", "ro", "ja"],
        test_case_id="7451",
        test_suite_id="242",
        blocked_by={"id": "4557 ", "platform": OSPlatform.WINDOWS},
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_30_pattern = LocationBar.URLBAR_ZOOM_BUTTON_30.similar(0.7)
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110
        urlbar_zoom_button_300_pattern = LocationBar.URLBAR_ZOOM_BUTTON_300

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Page successfully loaded, firefox logo found."

        region = create_region_for_url_bar()

        expected = exists(
            url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT, region=region
        )
        assert expected, "Zoom indicator not displayed by default in the url bar."

        zoom_in()

        new_region = create_region_for_url_bar()

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, "Zoom level successfully increased, zoom indicator found in the url bar."

        firefox.restart(url=LocalWeb.FIREFOX_TEST_SITE, image=LocalWeb.FIREFOX_LOGO)

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, "Zoom controls still displayed in the url bar after browser restart."

        zoom_out()

        select_location_bar()

        expected = exists(
            url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT, region=new_region
        )
        assert expected, (
            "Zoom level successfully decreased, zoom indicator not found in the url bar " "for 100% zoom level."
        )

        for i in range(8):
            zoom_in()

        expected = exists(urlbar_zoom_button_300_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, "Zoom level successfully increased, maximum zoom level(300%) reached."

        zoom_in()

        expected = exists(urlbar_zoom_button_300_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, "Zoom indicator still displays 300%."

        for i in range(8):
            zoom_out()

        expected = exists(
            url_bar_default_zoom_level_pattern.similar(0.92), FirefoxSettings.FIREFOX_TIMEOUT, region=new_region
        )
        assert expected, (
            "Zoom level successfully decreased, zoom indicator not found in the url bar " "for 100% zoom level."
        )

        for i in range(5):
            zoom_out()

        expected = exists(urlbar_zoom_button_30_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, "Zoom level successfully decreased, minimum zoom level(30%) reached."

        zoom_out()

        expected = exists(urlbar_zoom_button_30_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, "Zoom indicator still displays 30%."
