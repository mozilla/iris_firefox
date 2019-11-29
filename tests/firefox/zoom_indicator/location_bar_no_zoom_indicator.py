# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case checks that no zoom indicator is displayed in the location bar for the default "
        "zoom level.",
        locale=["en-US", "zh-CN", "es-ES", "de", "fr", "ru", "ko", "pt-PT", "vi", "pl", "tr", "ro", "ja"],
        test_case_id="7444",
        test_suite_id="242",
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Page successfully loaded, firefox logo found."

        region = create_region_for_url_bar()

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, "Zoom indicator not displayed by default in the url bar."
