# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Back from the Bookmarks menu'
        self.test_case_id = '165473'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        library_icon_pattern = NavBar.LIBRARY_MENU
        bookmarks_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        library_back_button_pattern = Utils.LIBRARY_BACK_BUTTON
        bookmarking_tools_pattern = LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS

        library_icon_exists = exists(library_icon_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_icon_exists, ' View history, saved bookmarks and more section button exists')

        click(library_icon_pattern)

        bookmarks_option_exists = exists(bookmarks_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_option_exists, 'The Bookmarks option exists')

        click(bookmarks_option_pattern)

        bookmark_menu_exists = exists(bookmarking_tools_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmark_menu_exists, 'The Bookmarks menu is correctly displayed.')

        library_back_button_exists = exists(library_back_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_back_button_exists, 'Button back exists')

        click(library_back_button_pattern)

        menu_exists = exists(bookmarks_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, menu_exists, 'View history, saved bookmarks and more section is displayed.')





