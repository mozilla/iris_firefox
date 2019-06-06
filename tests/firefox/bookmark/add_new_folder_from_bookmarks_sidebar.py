# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new folder from the Bookmarks Sidebar',
        locale=['en-US'],
        test_case_id='168931',
        test_suite_id='2525'
    )
    def run(self, firefox):
        new_folder_option_pattern = Library.Organize.NEW_FOLDER
        new_folder_created_pattern = Pattern('new_folder_is_created.png')
        new_folder_panel_pattern = Pattern('new_folder_panel.png')

        if not OSHelper.is_mac():
            bookmarks_menu_pattern = Library.BOOKMARKS_MENU
        else:
            bookmarks_menu_pattern = Pattern('bookmark_menu_section.png')

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, FirefoxSettings.FIREFOX_TIMEOUT/2)
        assert bookmarks_sidebar_menu_exists is True, 'Bookmarks Sidebar is correctly displayed.'

        bookmarks_menu_exists = exists(bookmarks_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT/2)
        assert bookmarks_menu_exists is True, 'Bookmarks menu section exists'

        right_click(bookmarks_menu_pattern)

        new_folder_option_exists = exists(new_folder_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT/2)
        assert new_folder_option_exists is True, 'New Folder option exists'

        click(new_folder_option_pattern)

        new_folder_panel_exists = exists(new_folder_panel_pattern, FirefoxSettings.FIREFOX_TIMEOUT/2)
        assert new_folder_panel_exists is True, 'The New Folder window is opened'

        type(Key.ENTER)

        click(bookmarks_menu_pattern)

        new_folder_created_exists = exists(new_folder_created_pattern, FirefoxSettings.FIREFOX_TIMEOUT/2)
        assert new_folder_created_exists is True, 'The New Folder is correctly created in the selected section.'
