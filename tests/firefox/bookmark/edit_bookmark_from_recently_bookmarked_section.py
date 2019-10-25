# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Edit a bookmark from the Recently Bookmarked section",
        locale=["en-US"],
        test_case_id="165492",
        test_suite_id="2525",
        profile=Profiles.TEN_BOOKMARKS,
        blocked_by={"id": "1527258", "platform": OSPlatform.WINDOWS},
    )
    def run(self, firefox):
        properties_option_pattern = Pattern("properties_option.png")
        new_modified_bookmark_pattern = Pattern("wiki_new_name_bookmark.png")
        name_before_editing_pattern = Pattern("name_field.png").similar(0.07)
        location_before_editing_pattern = Pattern("location_field.png")
        tags_before_editing_pattern = Pattern("tags_field.png").similar(0.7)
        keyword_before_editing_pattern = Pattern("keyword_field.png")

        if OSHelper.is_mac():
            bookmark_getting_started_pattern = Pattern(
                "bookmark_from_recently_bookmarked.png"
            )
        else:
            properties_window_pattern = Pattern("properties_window.png")
            bookmark_getting_started_pattern = Pattern("toolbar_bookmark_icon.png")

        library_button_exists = exists(
            NavBar.LIBRARY_MENU, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            library_button_exists is True
        ), "View history, saved bookmarks and more section exists"

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(
            Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_ICON,
            FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
        )
        assert (
            bookmarks_menu_option_exists is True
        ), "The Bookmarks menu is correctly displayed"

        click(Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_ICON)

        bookmark_getting_started_exists = exists(
            bookmark_getting_started_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            bookmark_getting_started_exists is True
        ), "Getting started bookmark exists"

        right_click(bookmark_getting_started_pattern)

        properties_option_exists = exists(
            properties_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert properties_option_exists is True, "Properties option exists"

        click(properties_option_pattern)

        if not OSHelper.is_mac():
            properties_window_exists = exists(
                properties_window_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
            )
            assert (
                properties_window_exists is True
            ), 'Properties for "Getting Started" window is opened'
        else:
            properties_window_exists = exists(
                name_before_editing_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
            )
            assert (
                properties_window_exists is True
            ), 'Properties for "Getting Started" window is opened'

        name_before_exists = exists(
            name_before_editing_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert name_before_exists is True, "Name field exists"

        location_before_exists = exists(
            location_before_editing_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert location_before_exists is True, "Location field exists"

        tags_before_exists = exists(
            tags_before_editing_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert tags_before_exists is True, "Tags field exists"

        keyword_before_exists = exists(
            keyword_before_editing_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert keyword_before_exists is True, "Keyword field exists"

        paste("New Name")
        type(Key.TAB)

        paste("wikipedia.org")
        type(Key.TAB)

        paste("Tag")

        if OSHelper.is_mac():
            type(Key.TAB)
        else:
            [type(Key.TAB) for _ in range(2)]

        paste("test")

        type(Key.ENTER)

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(
            Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_ICON,
            FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
        )
        assert (
            bookmarks_menu_option_exists is True
        ), "The Bookmarks menu is correctly displayed"

        click(Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_ICON)

        new_modified_bookmark_exists = exists(
            new_modified_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert new_modified_bookmark_exists is True, "New modified bookmark exists"

        right_click(new_modified_bookmark_pattern)

        properties_option_exists = exists(
            properties_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert properties_option_exists is True, "Properties option exists"

        click(properties_option_pattern)

        name_is_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert name_is_edited == "New Name", "Bookmark's name is edited"

        type(Key.TAB)

        location_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert (
            location_edited == "http://wikipedia.org/"
        ), "Bookmark's location is edited"

        type(Key.TAB)

        tags_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert tags_edited == "Tag", "Bookmark's tags are edited"

        if OSHelper.is_mac():
            type(Key.TAB)
        else:
            [type(Key.TAB) for _ in range(2)]

        keyword_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert keyword_edited == "test", "Bookmark's keywords are edited"
