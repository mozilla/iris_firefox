# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This is a test case that checks the zoom indicator + window state.",
        locale=["en-US"],
        test_case_id="7449",
        test_suite_id="242",
        blocked_by={"id": "4562", "platform": OSPlatform.WINDOWS},
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110
        urlbar_zoom_button_300_pattern = LocationBar.URLBAR_ZOOM_BUTTON_300

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Page successfully loaded, firefox logo found."

        region = create_region_for_url_bar()

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, "Zoom indicator not displayed by default in the url bar."

        zoom_in()

        new_region = create_region_for_url_bar()

        expected = exists(urlbar_zoom_button_110_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, "Zoom level successfully increased, zoom indicator found in the url bar."

        for i in range(7):
            zoom_in()

        expected = exists(urlbar_zoom_button_300_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, "Zoom level successfully increased, maximum zoom level(300%) reached."

        minimize_window()

        if OSHelper.is_windows() or OSHelper.is_linux():
            minimize_window()

        try:
            expected = wait_vanish(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, "Window successfully minimized."
        except FindError:
            raise FindError("Window not minimized.")

        restore_window_from_taskbar()

        if OSHelper.is_windows() or OSHelper.is_linux():
            maximize_window()

        expected = exists(NavBar.HAMBURGER_MENU, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Window successfully opened again."

        expected = exists(urlbar_zoom_button_300_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, "Zoom indicator still display 300%."
