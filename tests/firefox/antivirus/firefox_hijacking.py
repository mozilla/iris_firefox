# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Firefox hijacking.",
        locale=["en-US"],
        test_case_id="217858",
        test_suite_id="3063",
    )
    def run(self, firefox):
        about_preferences_search_pattern = Pattern("about_preferences_search.png")
        about_preferences_home_pattern = Pattern("about_preferences_home.png")
        default_search_engine_pattern = Pattern("default_search_engine.png")
        firefox_home_default_pattern = Pattern("firefox_home_default.png")
        search_suggestions_default_pattern = Pattern("search_suggestions_default.png")
        search_result_default_pattern = Pattern("search_result_default.png")
        top_sites_pattern = Pattern("top_sites.png")
        this_time_search_with_pattern = Pattern("this_time_search_with.png")
        ebay_one_off_button_pattern = Pattern("ebay_one_off_button.png")

        navigate("about:preferences#search")

        assert exists(
            about_preferences_search_pattern, 10
        ), "About preferences search page is successfully opened."
        assert exists(
            default_search_engine_pattern.similar(0.6), 10
        ), "The default search engine is not changed."

        new_tab()

        navigate("about:preferences#home")

        assert exists(
            about_preferences_home_pattern, 10
        ), "About preferences home page is successfully opened."
        assert exists(
            firefox_home_default_pattern.similar(0.6), 10
        ), "The default home page is not changed."

        click(NavBar.HOME_BUTTON)

        assert exists(Tabs.NEW_TAB_HIGHLIGHTED, 10) and exists(
            top_sites_pattern
        ), "The set homepage is opened."

        paste("text")

        one_off_bar_displayed = exists(
            this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        this_time_search_location = find(this_time_search_with_pattern)
        this_time_width, this_time_height = this_time_search_with_pattern.get_size()
        this_time_search_region = Region(
            this_time_search_location.x,
            this_time_search_location.y,
            this_time_width * 3,
            this_time_height,
        )

        ebay_one_off_displayed = exists(
            ebay_one_off_button_pattern,
            FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
            this_time_search_region,
        )

        if ebay_one_off_displayed:
            assert exists(
                search_suggestions_default_pattern, 10
            ), "The search suggestions dropdown is displayed, no extra search engines are added."
        else:
            assert exists(
                search_suggestions_default_pattern, 10
            ), "The search suggestions dropdown is displayed, no extra search engines are added."

        type(Key.ENTER)
        assert exists(
            search_result_default_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT
        ), "Search results displayed, with the known/selected search-engine."
