# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Hide Bookmarks Sidebar\' from Bookmarking Tools',
        locale=['en-US'],
        test_case_id='165479',
        test_suite_id='2525'
    )
    def run(self, firefox):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        bookmarking_tools_pattern = LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS
        view_bookmarks_sidebar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_SIDEBAR
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_sidebar_menu_pattern = SidebarBookmarks.BOOKMARKS_HEADER
        add_bookmarks_menu_to_toolbar_pattern = Pattern('add_bookmarks_menu_to_toolbar.png')
        hide_bookmarks_sidebar_pattern = Pattern('hide_bookmarks_sidebar.png')

        library_button_exists = exists(library_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_menu_option_exists is True, 'Bookmarks menu option exists'

        click(bookmarks_menu_option_pattern)

        bookmarking_tools_exists = exists(bookmarking_tools_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarking_tools_exists is True, 'The Bookmarks menu is correctly displayed'

        click(bookmarking_tools_pattern)

        add_bookmarks_menu_to_toolbar_exists = exists(add_bookmarks_menu_to_toolbar_pattern,
                                                      FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert add_bookmarks_menu_to_toolbar_exists is True, 'Bookmarking Tools window contains ' \
                                                             'Add Bookmarks Menu to Toolbar'

        view_bookmarks_sidebar_exists = exists(view_bookmarks_sidebar_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert view_bookmarks_sidebar_exists is True, 'Bookmarking Tools window contains View Bookmarks Sidebar'

        view_bookmarks_toolbar_exists = exists(view_bookmarks_toolbar_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert view_bookmarks_toolbar_exists is True, 'Bookmarking Tools window contains View Bookmarks Toolbar'

        click(view_bookmarks_sidebar_pattern)

        try:
            bookmarking_tools_not_exists = wait_vanish(view_bookmarks_sidebar_pattern,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert bookmarking_tools_not_exists is True, 'Bookmarking Tools window is dismissed'
        except FindError:
            raise FindError('Bookmarking Tools window is not dismissed')

        bookmarks_sidebar_menu_exists = exists(bookmarks_sidebar_menu_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_sidebar_menu_exists is True, 'The Bookmarks Sidebar is correctly displayed inside the FF ' \
                                                      'window, on the left side.'

        library_button_exists = exists(library_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_button_exists is True, 'View history, saved bookmarks and more section still exists'

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_menu_option_exists is True, 'Bookmarks menu option still exists'

        click(bookmarks_menu_option_pattern)

        bookmarking_tools_exists = exists(bookmarking_tools_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarking_tools_exists is True, 'The Bookmarks menu is correctly displayed'

        click(bookmarking_tools_pattern)

        add_bookmarks_menu_to_toolbar_exists = exists(add_bookmarks_menu_to_toolbar_pattern,
                                                      FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert add_bookmarks_menu_to_toolbar_exists is True, 'Bookmarking Tools window contains Add Bookmarks' \
                                                             ' Menu to Toolbar'

        hide_bookmarks_sidebar_exists = exists(hide_bookmarks_sidebar_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert hide_bookmarks_sidebar_exists is True, 'Bookmarking Tools window contains Hide Bookmarks Sidebar'

        view_bookmarks_toolbar_exists = exists(view_bookmarks_toolbar_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert view_bookmarks_toolbar_exists is True, 'Bookmarking Tools window contains View Bookmarks Toolbar'

        click(hide_bookmarks_sidebar_pattern)

        try:
            bookmarks_sidebar_menu_exists = wait_vanish(bookmarks_sidebar_menu_pattern,
                                                        FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert bookmarks_sidebar_menu_exists is True, 'The bookmarks sidebar is dismissed'
        except FindError:
            raise FindError('The bookmarks sidebar is not dismissed')

        library_button_exists = exists(library_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_menu_option_exists is True, 'Bookmarks menu option exists'

        click(bookmarks_menu_option_pattern)

        bookmarking_tools_exists = exists(bookmarking_tools_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarking_tools_exists is True, 'The Bookmarks menu is correctly displayed'

        click(bookmarking_tools_pattern)

        view_bookmarks_sidebar_exists = exists(view_bookmarks_sidebar_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert view_bookmarks_sidebar_exists is True, 'The Hide Bookmarks Sidebar button changes its state to View ' \
                                                      'Bookmarks Sidebar'
