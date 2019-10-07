# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Search bar can be successfully added/removed from the toolbar",
        test_case_id="143589",
        test_suite_id="2241",
        locale=["en-US"],
    )
    def run(self, firefox):
        preferences_search_pattern = (
            AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN
        )
        add_search_bar_in_toolbar_deselected_pattern = Pattern(
            "add_search_bar_in_toolbar_deselected.png"
        )
        add_search_bar_in_toolbar_selected_pattern = Pattern(
            "add_search_bar_in_toolbar_selected.png"
        )
        use_address_bar_deselected_pattern = Pattern("use_address_bar_deselected.png")
        use_address_bar_selected_pattern = Pattern("use_address_bar_selected.png")

        # Open Firefox and go to about:preferences, "Search" section.
        navigate("about:preferences#search")

        preferences_search_loaded = exists(
            preferences_search_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert (
            preferences_search_loaded
        ), "The about:preferences page is successfully loaded."

        add_search_bar_in_toolbar_deselected = exists(
            add_search_bar_in_toolbar_deselected_pattern,
            FirefoxSettings.FIREFOX_TIMEOUT,
        )
        assert (
            add_search_bar_in_toolbar_deselected
        ), 'Option "Add search bar in toolbar" is deselected.'

        #  2 From "Search Bar" select the option "Add search bar in toolbar".

        click(add_search_bar_in_toolbar_deselected_pattern, 1)

        add_search_bar_in_toolbar_selected = exists(
            add_search_bar_in_toolbar_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            add_search_bar_in_toolbar_selected
        ), 'The option "Add search bar in toolbar" is successfully selected.'

        search_bar_displayed = exists(
            LocationBar.SEARCH_BAR_MAGNIFYING_GLASS,
            FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
            region=Screen.RIGHT_HALF,
        )
        assert search_bar_displayed, "Search bar is displayed"

        # 3 Go to about:preferences, "Search" section.
        new_tab()

        navigate("about:preferences#search")

        preferences_search_loaded = exists(
            preferences_search_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert (
            preferences_search_loaded
        ), "The about:preferences page is successfully loaded."

        # 4 From "Search Bar" select the option "Use the address bar for search and navigation".
        navigate("about:preferences#search")

        preferences_search_loaded = exists(
            preferences_search_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert (
            preferences_search_loaded
        ), "The about:preferences page is successfully loaded."

        use_address_bar_deselected = exists(
            use_address_bar_deselected_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            use_address_bar_deselected
        ), 'Option "Use the address bar for search and navigation" is available'

        click(use_address_bar_deselected_pattern, 1)

        use_address_bar_selected = exists(
            use_address_bar_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            use_address_bar_selected
        ), 'Option "Use the address bar for search and navigation" selected'

        try:
            search_bar_removed = wait_vanish(
                LocationBar.SEARCH_BAR.similar(0.95), region=Screen.UPPER_RIGHT_CORNER
            )
        except FindError:
            raise FindError("Search bar is not removed")

        assert (
            search_bar_removed
        ), "The search bar is removed from the right side of the address bar."
