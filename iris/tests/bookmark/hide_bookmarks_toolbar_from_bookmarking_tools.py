# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Hide Bookmarks Toolbar\' from Bookmarking Tools '
        self.test_case_id = '165481'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        bookmarking_tools_pattern = LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS
        view_bookmarks_sidebar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_SIDEBAR
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        add_bookmarks_menu_to_toolbar_pattern = Pattern('add_bookmarks_menu_to_toolbar.png')
        hide_bookmarks_toolbar_pattern = Pattern('hide_bookmarks_toolbar.png')

        library_button_exists = exists(library_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'Bookmarks menu option exists')

        click(bookmarks_menu_option_pattern)

        bookmarking_tools_exists = exists(bookmarking_tools_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarking_tools_exists, 'The Bookmarks menu is correctly displayed')

        click(bookmarking_tools_pattern)

        add_bookmarks_menu_to_toolbar_exists = exists(add_bookmarks_menu_to_toolbar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, add_bookmarks_menu_to_toolbar_exists, 'Bookmarking Tools window contains '
                                                                'Add Bookmarks Menu to Toolbar')

        view_bookmarks_sidebar_exists = exists(view_bookmarks_sidebar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, view_bookmarks_sidebar_exists, 'Bookmarking Tools window contains View Bookmarks Sidebar')

        view_bookmarks_toolbar_exists = exists(view_bookmarks_toolbar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, view_bookmarks_toolbar_exists, 'Bookmarking Tools window contains View Bookmarks Toolbar')

        click(view_bookmarks_toolbar_pattern)

        try:
            bookmarking_tools_not_exists = wait_vanish(view_bookmarks_toolbar_pattern)
            assert_true(self, bookmarking_tools_not_exists, 'Bookmarking Tools window is dismissed')
        except FindError:
            raise FindError('Bookmarking Tools window is not dismissed')

        bookmarks_toolbar_exists = exists(bookmarks_toolbar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_toolbar_exists, 'Bookmarks Toolbar is correctly displayed under the URL bar')

        library_button_exists = exists(library_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section still exists')

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'Bookmarks menu option still exists')

        click(bookmarks_menu_option_pattern)

        bookmarking_tools_exists = exists(bookmarking_tools_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarking_tools_exists, 'The Bookmarks menu is correctly displayed')

        click(bookmarking_tools_pattern)

        add_bookmarks_menu_to_toolbar_exists = exists(add_bookmarks_menu_to_toolbar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, add_bookmarks_menu_to_toolbar_exists, 'Bookmarking Tools window contains '
                                                                'Add Bookmarks Menu to Toolbar')
        view_bookmarks_sidebar_exists = exists(view_bookmarks_sidebar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, view_bookmarks_sidebar_exists, 'Bookmarking Tools window contains View Bookmarks Sidebar')

        hide_bookmarks_toolbar_exists = exists(hide_bookmarks_toolbar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, hide_bookmarks_toolbar_exists, 'Bookmarking Tools window contains Hide Bookmarks Toolbar')

        click(hide_bookmarks_toolbar_pattern)

        try:
            bookmarking_toolbar_not_exists = wait_vanish(bookmarks_toolbar_pattern)
            assert_true(self, bookmarking_toolbar_not_exists, 'The bookmarks toolbar is dismissed')
        except FindError:
            raise FindError('The bookmarks toolbar is not dismissed')

        library_button_exists = exists(library_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'Bookmarks menu option exists')

        click(bookmarks_menu_option_pattern)

        bookmarking_tools_exists = exists(bookmarking_tools_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarking_tools_exists, 'The Bookmarks menu is correctly displayed')

        click(bookmarking_tools_pattern)

        view_bookmarks_toolbar_exists = exists(view_bookmarks_toolbar_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, view_bookmarks_toolbar_exists, 'The Hide Bookmarks Toolbar button '
                                                         'changes its state to View Bookmarks Toolbar')
