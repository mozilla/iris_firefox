# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Search suggestions can be disabled.",
        locale=["en-US"],
        test_case_id="4273",
        test_suite_id="83",
    )
    def run(self, firefox):
        provide_search_suggestions_checked_pattern = Pattern("provide_search_suggestions_checked.png")
        provide_search_suggestions_unchecked_pattern = Pattern("provide_search_suggestions_unchecked.png")
        search_suggestions_not_displayed_search_bar_pattern = \
            Pattern("search_suggestions_are_disabled_search_bar.png").similar(0.7)
        search_suggestions_not_displayed_new_tab_pattern = \
            Pattern("search_suggestions_not_displayed_new_tab.png")
        add_search_bar_in_toolbar = Pattern("add_search_bar_in_toolbar.png")

        # Disable the search bar.
        navigate("about:preferences#search")

        add_search_bar_in_toolbar_exists = exists(add_search_bar_in_toolbar, FirefoxSettings.FIREFOX_TIMEOUT)
        assert add_search_bar_in_toolbar_exists, "Add search bar in toolbar option is not present"
        click(add_search_bar_in_toolbar)
        time.sleep(Settings.DEFAULT_SLOW_MOTION_DELAY)

        search_bar_enabled = exists(LocationBar.SEARCH_BAR_MAGNIFYING_GLASS, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_bar_enabled, "The search bar couldn't be enabled"

        provide_search_suggestions_checked_exists = exists(
            provide_search_suggestions_checked_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert provide_search_suggestions_checked_exists, "The 'Provide search suggestions' option couldn't be enabled."

        click(provide_search_suggestions_checked_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        provide_search_suggestions_unchecked_pattern_exists = exists(
            provide_search_suggestions_unchecked_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert provide_search_suggestions_unchecked_pattern_exists, \
            "The 'Provide search suggestions' option couldn't be disabled."

        # Type in some random text in the Search Bar and content search field.
        select_search_bar()
        type("test", interval=0.25)

        suggestions_search_not_displayed = exists(
            search_suggestions_not_displayed_search_bar_pattern,
            FirefoxSettings.FIREFOX_TIMEOUT,
        )
        assert suggestions_search_not_displayed, (
            "Search suggestions found for the input text in search bar, Assertion failed."
        )

        new_tab()
        type("test", interval=0.25)
        new_tab_search_region = Region(
            0,
            0,
            Screen.SCREEN_WIDTH / 2,
            Screen.SCREEN_HEIGHT // 3,
        )
        suggestions_content_not_displayed = exists(
            search_suggestions_not_displayed_new_tab_pattern,
            FirefoxSettings.FIREFOX_TIMEOUT,region=new_tab_search_region
        )
        assert suggestions_content_not_displayed, \
            "Search suggestions found for the input text in about:newtab, Assertion failed."

        # Enable Search bar
        navigate("about:preferences#search")
        click(provide_search_suggestions_unchecked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        provide_search_suggestions_checked_exists = exists(
            provide_search_suggestions_checked_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert provide_search_suggestions_checked_exists, "The 'Provide search suggestions' option couldn't be enabled."

        select_search_bar()
        type("test", interval=0.25)

        suggestions_search_displayed = exists(
            search_suggestions_not_displayed_search_bar_pattern,
            FirefoxSettings.TINY_FIREFOX_TIMEOUT,
        )
        assert suggestions_search_displayed is False, \
            "Search suggestions couldn't found for the input text in search bar."

        new_tab()

        type("test", interval=0.25)

        suggestions_content_displayed = exists(
            search_suggestions_not_displayed_new_tab_pattern,
            FirefoxSettings.TINY_FIREFOX_TIMEOUT, region=new_tab_search_region
        )
        assert suggestions_content_displayed is False, \
            "Search suggestions couldn't found for the input text in 'about:newtab'."
