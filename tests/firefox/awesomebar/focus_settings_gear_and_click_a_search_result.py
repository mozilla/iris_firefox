# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case clicks on a search result while the settings gear is focused.",
        locale=["en-US"],
        test_case_id="108264",
        test_suite_id="1902",
    )
    def run(self, firefox):
        search_settings_pattern = Pattern("search_settings.png")
        this_time_search_with_pattern = Pattern("this_time_search_with.png")
        settings_gear_highlighted_pattern = Pattern("settings_gear_highlighted.png")
        google_one_off_button_pattern = Pattern("google_one_off_button.png")
        google_search_results_pattern = Pattern("google_search_results.png")

        region = Screen().new_region(
            0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3
        )

        select_location_bar()
        type("abc", interval=0.25)

        one_off_bar_displayed = exists(
            this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        expected = region.exists(
            search_settings_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert expected, "The 'Search settings' button is displayed in the awesomebar."

        assert scroll_until_pattern_found(
            settings_gear_highlighted_pattern, type, (Key.DOWN,), 20, 1
        ), "The 'Search settings' button is highlighted."

        one_off_button_exists = exists(
            google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert one_off_button_exists, "The 'Google' one-off button found."

        click(google_one_off_button_pattern)

        search_results_available = exists(
            google_search_results_pattern.similar(0.7), FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert search_results_available, (
            "The page corresponding to the search result is opened NOT the "
            "about:preferences page"
        )
