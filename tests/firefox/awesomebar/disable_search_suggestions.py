# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case disables search suggestions in awesomebar.",
        locale=["en-US"],
        test_case_id="108263",
        test_suite_id="1902",
    )
    def run(self, firefox):
        search_settings_pattern = Pattern("search_settings.png")
        about_preferences_search_page_pattern = Pattern(
            "about_preferences_search_page.png"
        )
        show_search_suggestions_in_address_bar_results_checked_pattern = Pattern(
            "show_search_suggestions_in_address_bar_results_checked.png"
        ).similar(0.6)
        show_search_suggestions_in_address_bar_results_unchecked_pattern = Pattern(
            "show_search_suggestions_in_address_bar_results_unchecked.png"
        ).similar(0.6)
        this_time_search_with_pattern = Pattern("this_time_search_with.png")

        region = Screen().new_region(
            0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3
        )

        select_location_bar()
        paste("abc")

        one_off_bar_displayed = exists(
            this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        expected = region.exists(search_settings_pattern, 10)
        assert expected, "The 'Search settings' button is displayed in the awesomebar."

        click(search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected, "The 'about:preferences#search' page successfully loaded."

        expected = exists(
            show_search_suggestions_in_address_bar_results_checked_pattern, 10
        )
        assert expected, (
            "Checkbox displayed in front of the 'Show search suggestions in address bar "
            + "results' text is checked by default."
        )

        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        paste("abc")

        one_off_bar_displayed = exists(
            this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        type(Key.DOWN)
        edit_select_all()
        edit_copy()

        time.sleep(Settings.DEFAULT_UI_DELAY)

        assert (
            "abc" in get_clipboard() and get_clipboard() != "abc"
        ), "Search suggestion are listed in the Awesomebar"

        next_tab()

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected, "The 'about:preferences#search' page successfully loaded."

        expected = exists(
            show_search_suggestions_in_address_bar_results_checked_pattern, 10
        )
        assert expected, (
            "Checkbox displayed in front of the 'Show search suggestions in address bar "
            + "results' text is checked by default."
        )

        click(show_search_suggestions_in_address_bar_results_checked_pattern)

        expected = exists(
            show_search_suggestions_in_address_bar_results_unchecked_pattern, 10
        )
        assert expected, (
            "Checkbox displayed in front of the 'Show search suggestions in address bar "
            "results' text is unchecked."
        )

        previous_tab()
        select_location_bar()
        type(Key.DELETE)
        paste("abc")

        one_off_bar_displayed = exists(
            this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            one_off_bar_displayed
        ), "The one-off bar is displayed at the bottom of awesomebar drop-down"

        type(Key.DOWN)
        edit_select_all()
        edit_copy()

        time.sleep(Settings.DEFAULT_UI_DELAY)

        assert (
            "abc" not in get_clipboard()
        ), "Search suggestion are not listed in the Awesomebar"
