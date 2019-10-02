# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case disables one-off searches from the awesomebar.",
        locale=["en-US"],
        test_case_id="108258",
        test_suite_id="1902",
        blocked_by={"id": "issue_3845", "platform": OSPlatform.ALL},
    )
    def run(self, firefox):
        google_search_results_pattern = Pattern("google_search_results.png")
        url = LocalWeb.FIREFOX_TEST_SITE
        this_time_search_with = Pattern("this_time_search_with.png")
        twitter_one_off_button = Pattern("twitter_one_off_button.png")
        twitter_search_results_localhost = Pattern(
            "twitter_search_results_localhost.png"
        )
        twitter_search_results_localhost_2 = Pattern(
            "twitter_search_results_localhost_2.png"
        )

        region = Screen().new_region(
            0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3
        )

        navigate(url)

        firefox_logo_exists = exists(
            LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert firefox_logo_exists, "Page successfully loaded, firefox logo found."

        # Type a partial part of the above address and perform a search, in a new tab, using an one-off.
        select_location_bar()
        type("127", interval=0.25)

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        one_off_bar_displayed = exists(
            this_time_search_with, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        twitter_one_off_button_exists = exists(
            twitter_one_off_button, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert twitter_one_off_button_exists, "The 'Twitter' one-off button found."

        click(twitter_one_off_button)

        close_content_blocking_pop_up()

        twitter_search_results_localhost_exists = exists(
            twitter_search_results_localhost, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        ) or exists(
            twitter_search_results_localhost_2, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert twitter_search_results_localhost_exists, (
            "A new tab with 'Twitter' search results"
            " for the searched string is opened."
        )

        change_preference("browser.urlbar.oneOffSearches", "false")

        select_location_bar()
        type("moz test", interval=0.25)

        localhost_string_exists = exists(this_time_search_with)
        assert (
            localhost_string_exists is False
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        type(Key.ENTER)

        expected = region.exists(
            google_search_results_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            expected
        ), "The search is made using the default search engine which is Google."
