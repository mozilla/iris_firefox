# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a new folder from the Bookmarks Sidebar '
        self.test_case_id = '168931'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        new_folder_option_pattern = Library.Organize.NEW_FOLDER
        new_folder_created_pattern = Pattern('new_folder_is_created.png')
        new_folder_panel_pattern = Pattern('new_folder_panel.png')

        if not Settings.is_mac():
            bookmarks_menu_pattern = Library.BOOKMARKS_MENU
        else:
            bookmarks_menu_pattern = Pattern('bookmark_menu_section.png')

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_sidebar_menu_exists, 'Bookmarks Sidebar is correctly displayed.')

        bookmarks_menu_exists = exists(bookmarks_menu_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_exists, 'Bookmarks menu section exists')

        right_click(bookmarks_menu_pattern)

        new_folder_option_exists = exists(new_folder_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_folder_option_exists, 'New Folder option exists')

        click(new_folder_option_pattern)

        new_folder_panel_exists = exists(new_folder_panel_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_folder_panel_exists, 'The New Folder window is opened')

        type(Key.ENTER)

        click(bookmarks_menu_pattern)

        new_folder_created_exists = exists(new_folder_created_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_folder_created_exists, 'The New Folder is correctly created in the selected section.')
