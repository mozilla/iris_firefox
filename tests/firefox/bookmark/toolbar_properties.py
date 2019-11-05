# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="'Properties' from 'Bookmarks Toolbar'",
        locale=["en-US"],
        test_case_id="164376",
        test_suite_id="2525",
        profile=Profiles.TEN_BOOKMARKS,
    )
    def run(self, firefox):
        getting_started_toolbar_bookmark_pattern = Pattern("toolbar_bookmark_icon.png")
        renamed_toolbar_bookmark_pattern = Pattern("renamed_toolbar_bookmark.png")
        properties_popup_save_button_pattern = Pattern("save_bookmark_name.png").similar(0.7)
        bookmark_properties_option = Pattern("properties_option.png")

        open_bookmarks_toolbar()

        bookmarks_folder_available_in_toolbar = exists(
            getting_started_toolbar_bookmark_pattern
        )
        assert (
            bookmarks_folder_available_in_toolbar is True
        ), "The 'Bookmarks Toolbar' is enabled."

        right_click(getting_started_toolbar_bookmark_pattern)

        properties_option_available = exists(
            bookmark_properties_option, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert properties_option_available is True, (
            "'Properties' option in available in context menu after "
            "right-click at the bookmark in toolbar."
        )

        click(bookmark_properties_option)

        properties_opened = exists(
            properties_popup_save_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            properties_opened is True
        ), "Properties for 'Getting Started' window is opened."

        paste("New Name")

        [type(Key.TAB) for _ in range(2)]

        type('Tag')

        if OSHelper.is_mac():
            type(Key.TAB)
        else:
            [type(Key.TAB) for _ in range(2)]

        type('keyword')

        type(Key.ENTER)

        bookmarks_folder_available_in_toolbar = exists(
            renamed_toolbar_bookmark_pattern
        )
        assert (
            bookmarks_folder_available_in_toolbar is True
        ), "The 'Bookmarks Toolbar' is enabled."

        right_click(renamed_toolbar_bookmark_pattern)

        properties_option_available = exists(
            bookmark_properties_option, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert properties_option_available is True, (
            "'Properties' option in available in context menu after "
            "right-click at the bookmark in toolbar."
        )

        click(bookmark_properties_option)

        properties_opened = exists(
            properties_popup_save_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            properties_opened is True
        ), "Properties for 'Getting Started' window is opened."

        name_is_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert name_is_edited == "New Name", "Bookmark's name is edited"

        [type(Key.TAB) for _ in range(2)]

        tags_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert tags_edited == "Tag", "Bookmark's tags are edited"

        if OSHelper.is_mac():
            type(Key.TAB)
        else:
            [type(Key.TAB) for _ in range(2)]

        keyword_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert keyword_edited == "keyword", "Bookmark's keywords are edited"

        type(Key.ESC)
