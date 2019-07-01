# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Navigate through the History menu from the Bookmark toolbar.',
        locale=['en-US'],
        test_case_id='174032',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        history_pattern = Library.HISTORY
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        history_bookmarks_toolbar_pattern = Pattern('history_bookmarks_toolbar.png')

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)

        expected = exists(bookmarks_toolbar_most_visited_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Bookmarks Toolbar has been activated.'

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)
        expected = right_upper_corner.exists(iris_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Iris page is displayed in the History menu list.'

        try:
            wait(show_all_history_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Show All History option found.')
            click(show_all_history_pattern)
        except FindError:
            raise FindError('Show All History option is not present on the page, aborting.')

        expected = exists(history_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'History section is visible.'

        right_click_and_type(history_pattern, keyboard_action='c')

        click_window_control('close')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        right_click_and_type(bookmarks_toolbar_most_visited_pattern, keyboard_action='p')

        new_tab()

        expected = exists(history_bookmarks_toolbar_pattern)
        assert expected, 'History section is displayed in the Bookmarks Toolbar.'

        click(history_bookmarks_toolbar_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        # Navigate to a page from Today's history, in our case the Iris page.
        type(Key.DOWN)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        type(Key.RIGHT)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        type(Key.ENTER)

        expected = exists(LocalWeb.IRIS_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Iris page successfully loaded.'
