# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Firefox Home Content - Snippets can be enabled/disabled",
        locale=["en-US"],
        test_case_id="171442",
        test_suite_id="2241",
    )
    def run(self, firefox):
        snippets_options_pattern = Pattern("snippets_option.png")
        home_page_snippets_pattern = Pattern("home_page_snippets.png")

        navigate("about:preferences#home")

        preferences_page_opened = exists(
            AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED,
            FirefoxSettings.FIREFOX_TIMEOUT,
        )
        assert (
            preferences_page_opened
        ), "The about:preferences page is successfully loaded."

        hover_location = Location(Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

        hover(hover_location)

        scroll_down(100)

        snippets_option_exists = exists(
            snippets_options_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert snippets_option_exists, "The Snippets option is displayed."

        snippet_option_location = find(snippets_options_pattern)
        snippet_option_width, snippet_option_height = (
            snippets_options_pattern.get_size()
        )
        snippet_option_region = Region(
            snippet_option_location.x - snippet_option_width,
            snippet_option_location.y,
            snippet_option_width * 2,
            snippet_option_height,
        )

        snippets_option_selected = exists(
            AboutPreferences.CHECKED_BOX,
            FirefoxSettings.FIREFOX_TIMEOUT,
            snippet_option_region,
        )
        assert snippets_option_selected, "The option is selected by default."

        navigate("about:home")

        snippets_displayed = exists(
            home_page_snippets_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            snippets_displayed is True
        ), "The Snippets section is displayed underneath Highlights section."

        navigate("about:newtab")

        snippets_displayed = exists(
            home_page_snippets_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            snippets_displayed is True
        ), "The Snippets section is displayed underneath Highlights section."

        navigate("about:preferences#home")

        preferences_page_opened = exists(
            AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED,
            FirefoxSettings.FIREFOX_TIMEOUT,
        )
        assert (
            preferences_page_opened
        ), "The about:preferences page is successfully loaded."

        hover(hover_location)

        scroll_down(100)

        snippets_option_exists = exists(
            snippets_options_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert snippets_option_exists, "The Snippets option is displayed."

        snippet_option_location = find(snippets_options_pattern)
        snippet_option_width, snippet_option_height = (
            snippets_options_pattern.get_size()
        )
        snippet_option_region = Region(
            snippet_option_location.x - snippet_option_width,
            snippet_option_location.y,
            snippet_option_width * 2,
            snippet_option_height,
        )

        snippets_option_selected = exists(
            AboutPreferences.CHECKED_BOX,
            FirefoxSettings.FIREFOX_TIMEOUT,
            snippet_option_region,
        )
        assert snippets_option_selected, "The option is selected by default."

        click(AboutPreferences.CHECKED_BOX, region=snippet_option_region)

        snippets_option_selected = exists(
            AboutPreferences.UNCHECKED_BOX,
            FirefoxSettings.FIREFOX_TIMEOUT,
            snippet_option_region,
        )
        assert snippets_option_selected, "The options is not selected anymore."

        navigate("about:home")

        snippets_displayed = exists(
            home_page_snippets_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            snippets_displayed is False
        ), "The Snippets section is not displayed underneath Highlights section."

        navigate("about:newtab")

        snippets_displayed = exists(
            home_page_snippets_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            snippets_displayed is False
        ), "The Snippets section is not displayed underneath Highlights section."

        new_window()

        snippets_displayed = exists(
            home_page_snippets_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            snippets_displayed is False
        ), "The Snippets section is not displayed underneath Highlights section."

        new_private_window()

        private_window_opened = exists(
            PrivateWindow.private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert private_window_opened, "Private window opened"

        snippets_displayed = exists(
            home_page_snippets_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            snippets_displayed is False
        ), "The Snippets section is not displayed underneath Highlights section."
