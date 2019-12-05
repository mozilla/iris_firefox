# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Edit a bookmark from the Bookmarks Toolbar submenu",
        locale=["en-US"],
        test_case_id="163491",
        test_suite_id="2525",
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC,
        blocked_by={"id": "1527258", "platform": OSPlatform.WINDOWS},
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern("bookmarks_top_menu.png")
        firefox_menu_bookmarks_toolbar_pattern = Pattern("firefox_menu_bookmarks_toolbar.png")
        firefox_menu_most_visited_pattern = Pattern("firefox_menu_most_visited.png")
        getting_started_pattern = Pattern("getting_started_top_menu.png")
        properties_option_pattern = Pattern("properties_option.png")
        name_field_pattern = Pattern("name_bookmark_field.png").similar(0.7)
        location_field_pattern = Pattern("location_field_label.png").similar(0.7)
        tags_field_pattern = Pattern("tags_field_label.png").similar(0.7)
        keyword_field_pattern = Pattern("keyword_field_label.png").similar(0.7)

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists, "Firefox menu > Bookmarks exists"

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(
            firefox_menu_bookmarks_toolbar_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert bookmarks_toolbar_folder_exists is True, "Firefox menu > Bookmarks > Bookmarks Toolbar folder exists"

        click(firefox_menu_bookmarks_toolbar_pattern)

        most_visited_folder_exists = exists(firefox_menu_most_visited_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert most_visited_folder_exists is True, (
            "Firefox menu > Bookmarks > Bookmarks Toolbar > Most Visited " "folder exists"
        )

        getting_started_exists = exists(getting_started_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert getting_started_exists is True, (
            "Firefox menu > Bookmarks > Bookmarks Toolbar > Getting Started " "bookmark exists"
        )

        right_click(getting_started_pattern)

        properties_option_exists = exists(properties_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_option_exists is True, "Properties option exists"

        click(properties_option_pattern)

        bookmark_properties_opened = exists(name_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_properties_opened is True, "Bookmark properties window is opened"

        paste("Focus")
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.TAB)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        paste(LocalWeb.FOCUS_TEST_SITE)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.TAB)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        paste("tagfocus")
        time.sleep(Settings.DEFAULT_UI_DELAY)
        if OSHelper.is_mac():
            type(Key.TAB)
        else:
            type(Key.TAB)
            time.sleep(Settings.DEFAULT_UI_DELAY)
            type(Key.TAB)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        paste("keyfocus")
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        open_bookmarks_toolbar()

        bookmark_edited = exists(LocalWeb.FOCUS_BOOKMARK_SMALL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_edited is True, "The window is dismissed and all the changes are correctly saved"

        right_click(LocalWeb.FOCUS_BOOKMARK_SMALL)

        properties_option_exists = exists(properties_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_option_exists is True, "Properties option exists"

        click(properties_option_pattern)

        click(name_field_pattern)
        edit_select_all()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        name_text = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        expected_text = "Focus"
        assert name_text == expected_text, "Name is changed"

        click(location_field_pattern)
        edit_select_all()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        location_text = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        expected_text = LocalWeb.FOCUS_TEST_SITE
        assert location_text == expected_text, "Location is changed"

        tags_field_reachable = exists(tags_field_pattern)
        assert tags_field_reachable is True, "Tags field is reachable"

        click(tags_field_pattern)
        edit_select_all()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        tags_text = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        expected_text = "tagfocus"
        assert tags_text == expected_text, "Tags are edited"

        keywords_field_reachable = exists(keyword_field_pattern)
        assert keywords_field_reachable is True, "Keywords field is reachable"

        click(keyword_field_pattern)
        edit_select_all()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        keyword_text = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        expected_text = "keyfocus"
        assert keyword_text == expected_text, "Keywords are edited"

        type(Key.ESC)
