# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Paste a bookmark in 'Mozilla Firefox' section",
        locale=["en-US"],
        test_case_id="163378",
        test_suite_id="2525",
        exclude=OSPlatform.MAC,
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern("bookmarks_top_menu.png")
        mozilla_firefox_bookmarks_folder_pattern = Pattern(
            "mozilla_firefox_bookmarks_folder.png"
        )
        mozilla_about_us_bookmark_pattern = Pattern("mozilla_about_us_bookmark.png")
        open_all_in_tabs_pattern = Pattern("open_all_in_tabs.png")
        customize_firefox_bookmark_pattern = Pattern(
            "mozilla_customize_firefox_bookmark.png"
        )
        get_involved_bookmark_pattern = Pattern("mozilla_get_involved_bookmark.png")
        help_and_tutorials_bookmark_pattern = Pattern(
            "mozilla_help_and_tutorials_bookmark.png"
        )
        copy_option_pattern = Pattern("copy_option.png")
        paste_option_pattern = Pattern("paste_option.png")
        getting_started_in_toolbar_pattern = Pattern("getting_started_top_menu.png")
        bookmarks_toolbar_folder_pattern = Pattern("bookmark_toolbar_top_menu.png")

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(
            firefox_menu_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert firefox_menu_bookmarks_exists is True, "Firefox menu > Bookmarks exists"

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(
            bookmarks_toolbar_folder_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            bookmarks_toolbar_folder_exists is True
        ), "Bookmarks toolbar folder exists"

        click(bookmarks_toolbar_folder_pattern)

        getting_started_bookmark_exists = exists(
            getting_started_in_toolbar_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            getting_started_bookmark_exists is True
        ), "Getting started bookmark exists"

        right_click(getting_started_in_toolbar_pattern)

        copy_option_exists = exists(
            copy_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert copy_option_exists is True, "The Copy option exists"

        click(copy_option_pattern)

        mozilla_firefox_bookmarks_folder_exists = exists(
            mozilla_firefox_bookmarks_folder_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert mozilla_firefox_bookmarks_folder_exists is True, (
            "Firefox menu > Bookmarks > Mozilla Firefox " "bookmarks folder exists"
        )

        click(mozilla_firefox_bookmarks_folder_pattern)

        mozilla_customize_firefox_bookmark_exists = exists(
            customize_firefox_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            mozilla_customize_firefox_bookmark_exists is True
        ), "Customize Firefox bookmark is displayed"

        mozilla_get_involved_bookmark_exists = exists(get_involved_bookmark_pattern)
        assert (
            mozilla_get_involved_bookmark_exists is True
        ), "Get Involved bookmark is displayed"

        mozilla_help_and_tutorials_bookmark_exists = exists(
            help_and_tutorials_bookmark_pattern
        )
        assert (
            mozilla_help_and_tutorials_bookmark_exists is True
        ), "Help and Tutorials bookmark is displayed"

        mozilla_about_us_bookmark_exists = exists(mozilla_about_us_bookmark_pattern)
        assert (
            mozilla_about_us_bookmark_exists is True
        ), "About Us bookmark is displayed"

        open_all_in_tabs_exists = exists(open_all_in_tabs_pattern)
        assert open_all_in_tabs_exists is True, "Open all in tabs option exists"

        right_click(mozilla_about_us_bookmark_pattern)

        paste_option_exists = exists(
            paste_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert paste_option_exists is True, "Paste option exists"

        click(paste_option_pattern)

        bookmark_pasted = exists(
            getting_started_in_toolbar_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            bookmark_pasted is True
        ), "Bookmark is correctly pasted in selected section"

        restore_firefox_focus()
