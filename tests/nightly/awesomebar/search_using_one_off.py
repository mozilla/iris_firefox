# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.nightly.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case perform a search using a one-off focusing on the autocomplete drop-down.",
        locale=["en-US"],
        test_case_id="108249",
        test_suite_id="1902",
    )
    def run(self, firefox):
        page_bookmarked_pattern = Bookmarks.StarDialog.NEW_BOOKMARK
        search_suggestion_bookmarked_tab_pattern = Pattern("search_suggestion_bookmarked_tab.png")
        search_suggestion_opened_tab_pattern = Pattern("search_suggestion_opened_tab.png")
        search_suggestion_history_pattern = Pattern("search_suggestion_history.png")
        popular_search_suggestion_pattern = Pattern("popular_search_suggestion.png")
        google_one_off_button_pattern = Pattern("google_one_off_button.png").similar(0.9)
        google_search_results_pattern = Pattern("google_search_results.png").similar(0.6)

        region = Screen.TOP_THIRD

        new_tab()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, "Mozilla page loaded successfully."

        bookmark_page()

        expected = region.exists(page_bookmarked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Page was bookmarked."

        close_tab()

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, "Firefox page loaded successfully."

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        expected = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, "Focus page loaded successfully."

        close_tab()

        new_tab()

        select_location_bar()
        type("m")

        expected = exists(search_suggestion_bookmarked_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, "Bookmarked page found between search suggestions."

        select_location_bar()
        type("fi")

        expected = exists(search_suggestion_opened_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, "Opened tab found between search suggestions."

        select_location_bar()
        type("f")

        expected = exists(search_suggestion_history_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, "Web pages from personal browsing history found between search suggestions."

        expected = exists(popular_search_suggestion_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Popular search suggestions from the default search engine found between search suggestions."

        expected = exists(google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "The 'Google' one-off button found."

        click(google_one_off_button_pattern)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        expected = region.exists(google_search_results_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, "Google search results are displayed."
