# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarking Tools\' from bookmarks menu',
        locale=['en-US'],
        test_case_id='165476',
        test_suite_id='2525'
    )
    def run(self, firefox):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        bookmarking_tools_pattern = LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS
        view_bookmarks_sidebar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_SIDEBAR
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        add_bookmarks_menu_to_toolbar_pattern = Pattern('add_bookmarks_menu_to_toolbar.png')

        library_button_exists = exists(library_button_pattern)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern)
        assert bookmarks_menu_option_exists, 'Bookmarks menu option exists'

        click(bookmarks_menu_option_pattern)

        bookmarking_tools_exists = exists(bookmarking_tools_pattern)
        assert bookmarking_tools_exists is True, 'Bookmarking tools section exists'

        click(bookmarking_tools_pattern)

        add_bookmarks_menu_to_toolbar_exists = exists(add_bookmarks_menu_to_toolbar_pattern)
        assert add_bookmarks_menu_to_toolbar_exists is True, 'Add Bookmarks Menu to Toolbar is displayed'

        view_bookmarks_sidebar_exists = exists(view_bookmarks_sidebar_pattern)
        assert view_bookmarks_sidebar_exists is True, 'View Bookmarks Sidebar is displayed'

        view_bookmarks_toolbar_exists = exists(view_bookmarks_toolbar_pattern)
        assert view_bookmarks_toolbar_exists is True, 'View Bookmarks Toolbar is displayed'
