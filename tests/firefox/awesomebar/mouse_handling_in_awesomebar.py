# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Mouse handling - in the awesomebar.",
        locale=["en-US"],
        test_case_id="108282",
        test_suite_id="1902",
    )
    def run(self, firefox):
        twitter_one_off_button_highlight_pattern = Pattern(
            "twitter_one_off_button_highlight.png"
        )
        search_suggestion_opened_tab_pattern = Pattern(
            "search_suggestion_opened_tab.png"
        ).similar(0.7)
        search_settings_pattern = Pattern("search_settings.png")
        settings_gear_highlighted_pattern = Pattern("settings_gear_highlighted.png")

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Firefox page loaded successfully."

        new_tab()

        select_location_bar()
        paste("127")

        # Press "Alt" and arrow up keys to select an one-off button and hover over it.
        if OSHelper.is_linux():
            repeat_key_up(3)
        else:
            type(text=Key.UP, modifier=KeyModifier.ALT)
            type(text=Key.UP, modifier=KeyModifier.ALT)

        expected = exists(
            twitter_one_off_button_highlight_pattern,
            FirefoxSettings.FIREFOX_TIMEOUT,
            region,
        )
        assert expected, "The 'Twitter' one-off button is highlighted."

        hover(twitter_one_off_button_highlight_pattern)

        expected = exists(
            twitter_one_off_button_highlight_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            expected
        ), "The 'Twitter' one-off button is still highlighted in the previous color."

        # Without closing the autocomplete drop-down, move mouse over an one-off button.
        expected = exists(search_settings_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "The 'Search settings' button is displayed in the awesomebar."

        hover(search_settings_pattern)

        expected = exists(settings_gear_highlighted_pattern.similar(0.9))
        assert (
            expected is False
        ), "Successfully hovered over the 'Search settings'  one off."

        # Hover over an autocomplete result that is not selected and click on it.
        expected = exists(
            search_suggestion_opened_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert expected, "Opened tab found between the search suggestions."

        click(search_suggestion_opened_tab_pattern)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert (
            expected
        ), "Clicking a result that is not the selected loads the clicked result, not the selected result."
