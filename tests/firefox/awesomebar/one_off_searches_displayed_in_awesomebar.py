# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case checks that one-off searches are displayed in the awesomebar.",
        locale=["en-US"],
        test_case_id="108248",
        test_suite_id="1902",
        blocked_by={"id": "issue_3845", "platform": OSPlatform.ALL},
    )
    def run(self, firefox):
        search_settings_pattern = Pattern("search_settings.png")
        amazon_one_off_button_pattern = Pattern("amazon_one_off_button.png").similar(
            0.7
        )
        bing_one_off_button_pattern = Pattern("bing_one_off_button.png")
        duck_duck_go_one_off_button_pattern = Pattern("duck_duck_go_one_off_button.png")
        google_one_off_button_pattern = Pattern("google_one_off_button.png")
        twitter_one_off_button_pattern = Pattern("twitter_one_off_button.png")
        wikipedia_one_off_button_pattern = Pattern(
            "wikipedia_one_off_button.png"
        ).similar(0.6)
        this_time_search_with_pattern = Pattern("this_time_search_with.png")

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        select_location_bar()
        paste("abc")

        one_off_bar_displayed = exists(
            this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        pattern_list = [
            google_one_off_button_pattern,
            bing_one_off_button_pattern,
            twitter_one_off_button_pattern,
            wikipedia_one_off_button_pattern,
            amazon_one_off_button_pattern,
            duck_duck_go_one_off_button_pattern,
            search_settings_pattern,
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
