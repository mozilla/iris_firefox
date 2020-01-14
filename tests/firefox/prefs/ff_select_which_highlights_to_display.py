# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Firefox Home Content - Firefox can select which Highlights to display",
        test_case_id="161671",
        test_suite_id="2241",
        locale=["en-US"],
        blocked_by={"id": "4486", "platform": OSPlatform.ALL},

    )
    def run(self, firefox):
        about_preferences_home_url_pattern = Pattern("about_preferences_home_url.png")
        visited_page_checkbox = Pattern("visited_page_checkbox.png")
        bookmarks_checkbox = Pattern("bookmarks_checkbox.png")
        most_recent_download_checkbox = Pattern("most_recent_download_checkbox.png")
        pages_saved_to_pocket_checkbox = Pattern("pages_saved_to_pocket_checkbox.png")
        bookmark_highlights_new_tab = Pattern("bookmark_highlights_new_tab.png")
        download_history_button = Pattern("download_history_button.png").similar(0.6)
        most_recent_download_highlights_new_tab = Pattern("most_recent_download_highlights_new_tab.png")
        github_logo = Pattern("github_logo.png")
        recent_visited_highlights_new_tab = Pattern("recent_visited_highlights_new_tab.png")
        replace_button_duplicate_check = Pattern("replace_button_duplicate_check.png")
        mozilla_logo_full = Pattern("mozilla_logo_full.png")
        if OSHelper.is_linux():
            highlights_options_pattern = Pattern("highlights_search_result.png")
        else:
            highlights_options_pattern = Pattern("highlights_option.png")
        highlight_options = [
            visited_page_checkbox,
            bookmarks_checkbox,
            most_recent_download_checkbox,
            pages_saved_to_pocket_checkbox,
        ]
        # Pre-requisite for "Visited Pages" validation
        navigate("about:newtab")
        navigate("https://github.com/")

        github_page_loaded = exists(github_logo, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert github_page_loaded, "Github page could not be loaded successfully"

        # Pre-requisite for "Most Recent Download" validation
        navigate("about:newtab")
        navigate("https://www.mozilla.org/en-US/")
        mozilla_logo_full_exists = exists(mozilla_logo_full, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert mozilla_logo_full_exists, "Mozilla URL https://www.mozilla.org/en-US/' couldn't load"
        open_save_page()
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        type(Key.ENTER)
        if OSHelper.is_mac() or OSHelper.is_linux():
            replace_button_duplicate_check_exists = exists(
                replace_button_duplicate_check, FirefoxSettings.FIREFOX_TIMEOUT
            )
            if replace_button_duplicate_check_exists:
                click(replace_button_duplicate_check)
        else:
            type(text="y", modifier=KeyModifier.ALT)
        download_history_button_exists = exists(download_history_button, FirefoxSettings.FIREFOX_TIMEOUT)
        assert download_history_button_exists, "Download button doesn't appear"
        click(download_history_button)

        navigate("about:preferences#home")
        about_preferences_home_url_exists = exists(about_preferences_home_url_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert (
            about_preferences_home_url_exists
        ), "Home section of about:preferences page could not be loaded successfully"

        click(AboutPreferences.FIND_IN_OPTIONS)
        paste("Highlights")

        preferences_page_opened = exists(highlights_options_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, "Highlights section is not present in the about:preferences page."

        highlights_option_location = find(highlights_options_pattern)
        highlights_option_width, highlights_option_height = highlights_options_pattern.get_size()
        highlights_option_region = Region(
            highlights_option_location.x - highlights_option_width,
            highlights_option_location.y - highlights_option_height / 2,
            highlights_option_width * 2,
            highlights_option_height * 2,
        )

        highlights_option_selected = exists(
            AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT, highlights_option_region
        )
        assert highlights_option_selected, "Checkbox option present in 'Highlights' is not selected by default"

        for highlights in highlight_options:
            highlights_option_checkbox = exists(highlights)
            assert (
                highlights_option_checkbox
            ), "Checkbox option is not present either of Visited Pages or " "Bookmarks or Most Recent Download or Pages Saved to Pocket"

        # "Visited Pages" validation
        click(bookmarks_checkbox)
        click(most_recent_download_checkbox)
        click(pages_saved_to_pocket_checkbox)
        navigate("about:newtab")
        recent_visited_highlights_new_tab_exists = exists(
            recent_visited_highlights_new_tab, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert recent_visited_highlights_new_tab_exists, "Most recent download page is not displayed in Highlights"

        # Bookmark Validation
        navigate("about:preferences#home")
        click(AboutPreferences.FIND_IN_OPTIONS)
        paste("Highlights")
        click(visited_page_checkbox)
        click(bookmarks_checkbox)

        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED
        new_tab()
        navigate("https://mozillians.org/en-US/")

        bookmark_button_pattern_exists = exists(bookmark_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_button_pattern_exists, "Bookmark star is not present on the page"
        click(bookmark_button_pattern)

        page_bookmarked_assert = exists(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_bookmarked_assert, "The page was successfully bookmarked via the star button."

        navigate("about:newtab")
        bookmark_highlights_new_tab_exists = exists(bookmark_highlights_new_tab, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_highlights_new_tab_exists, "Bookmarks page is not displayed in Highlights"

        # "Most Recent Download" validation
        previous_tab()
        click(bookmarks_checkbox)
        click(most_recent_download_checkbox)
        navigate("about:newtab")
        most_recent_download_highlights_new_tab_exists = exists(
            most_recent_download_highlights_new_tab, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            most_recent_download_highlights_new_tab_exists
        ), "Downloaded page or Saved page is not displayed in Highlights"

    # Pocket testing has been removed from the scope of this test case.
