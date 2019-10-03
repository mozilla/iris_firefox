# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case perform a search by keyboard only.",
        locale=["en-US"],
        test_case_id="108268",
        test_suite_id="1902",
        profile_preferences={"browser.contentblocking.enabled": False},
        blocked_by={"id": "issue_3845", "platform": OSPlatform.ALL},
    )
    def run(self, firefox):
        this_time_search_with_pattern = Pattern("this_time_search_with.png")
        twitter_search_results_localhost = Pattern(
            "twitter_search_results_localhost.png"
        )
        twitter_search_results_localhost_2 = Pattern(
            "twitter_search_results_localhost_2.png"
        )
        if OSHelper.is_mac() or OSHelper.is_windows():
            twitter_one_off_button_highlight_pattern = Pattern(
                "twitter_one_off_button_highlight.png"
            ).similar(0.99)
            bing_one_off_button_highlight_pattern = Pattern(
                "bing_one_off_button_highlight.png"
            ).similar(0.95)
        elif OSHelper.is_windows():
            twitter_one_off_button_highlight_pattern = Pattern(
                "twitter_one_off_button_highlight.png"
            ).similar(0.9)
            bing_one_off_button_highlight_pattern = Pattern(
                "bing_one_off_button_highlight.png"
            ).similar(0.95)
        else:
            twitter_one_off_button_highlight_pattern = Pattern(
                "twitter_one_off_button_highlight.png"
            ).similar(0.9)
            bing_one_off_button_highlight_pattern = Pattern(
                "bing_one_off_button_highlight.png"
            ).similar(0.95)
        bing_search_results_pattern = Pattern("bing_search_results_localhost.png")
        duck_one_off_button_highlight_pattern = Pattern(
            "duck_one_off_button_highlight.png"
        ).similar(0.9)
        duck_go_search_result_pattern = Pattern("duck_go_search_result.png").similar(
            0.7
        )

        select_location_bar()
        paste("127")

        one_off_bar_displayed = exists(
            this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        assert scroll_until_pattern_found(
            twitter_one_off_button_highlight_pattern, type, (Key.UP,), 20, 1
        ), "The 'Twitter' button is highlighted."

        type(Key.ENTER)

        twitter_search_results_localhost_exists = exists(
            twitter_search_results_localhost, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        ) or exists(
            twitter_search_results_localhost_2, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert twitter_search_results_localhost_exists, (
            "A new tab with 'Twitter' search results"
            " for the searched string is opened."
        )

        click(NavBar.HOME_BUTTON.target_offset(400, 0))
        edit_select_all()
        paste("127.0")

        one_off_bar_displayed = exists(
            this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        assert scroll_until_pattern_found(
            bing_one_off_button_highlight_pattern, type, (Key.UP,), 20, 1
        ), "The 'Bing' button is highlighted."

        type(Key.ENTER)

        bing_search_results_localhost_exists = exists(
            bing_search_results_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            bing_search_results_localhost_exists
        ), "'Bing' search results are opened in the same tab."

        select_location_bar()
        paste("127.0")

        one_off_bar_displayed = exists(
            this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        assert scroll_until_pattern_found(
            duck_one_off_button_highlight_pattern, type, (Key.UP,), 20, 1
        ), "The 'Duck-duck-go' button is highlighted."

        type(Key.ENTER)

        bing_search_results_localhost_exists = exists(
            duck_go_search_result_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            bing_search_results_localhost_exists
        ), "'Duck-duck-go' search results are opened in the same tab."
