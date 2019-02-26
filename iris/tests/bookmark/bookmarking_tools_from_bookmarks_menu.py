# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarking Tools\' from bookmarks menu'
        self.test_case_id = '165476'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        bookmarking_tools_pattern = LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS
        view_bookmarks_sidebar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_SIDEBAR
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        add_bookmarks_menu_to_toolbar_pattern = Pattern('add_bookmarks_menu_to_toolbar.png')

        library_button_exists = exists(library_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'Bookmarks menu option exists')

        click(bookmarks_menu_option_pattern)

        bookmarking_tools_exists = exists(bookmarking_tools_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarking_tools_exists, 'Bookmarking tools section exists')

        click(bookmarking_tools_pattern)

        add_bookmarks_menu_to_toolbar_exists = exists(add_bookmarks_menu_to_toolbar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, add_bookmarks_menu_to_toolbar_exists, 'Add Bookmarks Menu to Toolbar is displayed')

        view_bookmarks_sidebar_exists = exists(view_bookmarks_sidebar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, view_bookmarks_sidebar_exists, 'View Bookmarks Sidebar is displayed')

        view_bookmarks_toolbar_exists = exists(view_bookmarks_toolbar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, view_bookmarks_toolbar_exists, 'View Bookmarks Toolbar is displayed')
