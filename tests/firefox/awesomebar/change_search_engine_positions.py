# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case verifies that changing the search engines positions the change is applied in "
        "awesome bar too.",
        locale=["en-US"],
        test_case_id="108262",
        test_suite_id="1902",
    )
    def run(self, firefox):
        search_engine_pattern = Pattern("search_engine.png")
        search_settings_pattern = Pattern("search_settings.png")
        amazon_one_off_button_pattern = Pattern("amazon_one_off_button.png")
        bing_one_off_button_pattern = Pattern("bing_one_off_button.png")
        duck_duck_go_one_off_button_pattern = Pattern("duck_duck_go_one_off_button.png")
        google_one_off_button_pattern = Pattern("google_one_off_button.png")
        twitter_one_off_button_pattern = Pattern("twitter_one_off_button.png")
        wikipedia_one_off_button_pattern = Pattern("wikipedia_one_off_button.png")
        about_preferences_search_page_pattern = Pattern(
            "about_preferences_search_page.png"
        )
        google_search_engine_pattern = Pattern("google_search_engine.png")
        duckduckgo_search_engine_pattern = Pattern("duckduckgo_search_engine.png")

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        select_location_bar()
        type("moz", interval=0.25)

        pattern_list = [
            google_one_off_button_pattern,
            bing_one_off_button_pattern,
            twitter_one_off_button_pattern,
            wikipedia_one_off_button_pattern,
            amazon_one_off_button_pattern,
            duck_duck_go_one_off_button_pattern,
        ]

        # Deleted assert for ebay because we no longer have the ebay search engine in place in some locations.

        # Check that the one-off list is displayed in the awesomebar.
        for i in range(pattern_list.__len__()):
            if OSHelper.is_mac():
                expected = region.exists(pattern_list[i].similar(0.7), 10)
                assert expected, (
                    "Element found at position " + i.__str__() + " in the list found."
                )
            else:
                expected = region.exists(pattern_list[i].similar(0.9), 10)
                assert expected, (
                    "Element found at position " + i.__str__() + " in the list found."
                )

        google_one_off_location = find(google_one_off_button_pattern)
        bing_one_off_location = find(bing_one_off_button_pattern)

        # Navigate to the about:preferences#search page and reorder the search engines.
        search_settings_button_displayed = exists(
            search_settings_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert search_settings_button_displayed, "Search settings button displayed"

        click(search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected, "The 'about:preferences#search' page successfully loaded."

        paste("one-click")

        expected = exists(search_engine_pattern, 10)
        assert expected, "One-Click Search Engines section found."

        drag_drop(duckduckgo_search_engine_pattern, google_search_engine_pattern)

        # Make sure that the one-off buttons are reordered in the awesomebar.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        type("moz", interval=0.25)

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        google_one_off_reoredered_location = find(google_one_off_button_pattern)
        bing_one_off_reoredered_location = find(bing_one_off_button_pattern)
        duck_duck_go_one_off_reoredered_location = find(
            duck_duck_go_one_off_button_pattern
        )

        assert (
            google_one_off_reoredered_location.x == google_one_off_location.x
        ), "The 'Google' one-off search engine still holds the first position in the one-offs list after reorder."

        assert (
            bing_one_off_location.x != bing_one_off_reoredered_location.x
        ), "The 'Bing' one-off search engine changed position in the one-offs list after reorder."

        assert (
            duck_duck_go_one_off_reoredered_location.x
            > google_one_off_reoredered_location.x
            and duck_duck_go_one_off_reoredered_location.x
            < bing_one_off_reoredered_location.x
        ), "The 'DuckDuckGo' one-off search engine holds the second position in the one-offs list after reorder."
